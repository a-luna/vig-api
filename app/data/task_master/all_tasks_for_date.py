import os
import re
import subprocess
from datetime import datetime
from functools import cached_property
from pathlib import Path

from halo import Halo

import vigorish.database as db
from task_master.convert_seasons import convert_mlb_api_data_for_date
from task_master.task_config_settings import TaskConfigSettings
from task_master.scrape_mlb_game_feed import scrape_mlb_api_data_for_date
from vigorish.cli.components.util import print_heading
from vigorish.constants import DATA_SET_TO_NAME_MAP
from vigorish.app import Vigorish
from vigorish.enums import DataSet, StatusReport
from vigorish.scrape.job_runner import JobRunner
from vigorish.cli.components import get_random_dots_spinner, get_random_cli_color
from vigorish.cli.menu_items import CombineScrapedData
from vigorish.status.update_status_bbref_boxscores import update_status_bbref_boxscore_list
from vigorish.status.update_status_bbref_games_for_date import update_bbref_games_for_date_list
from vigorish.status.update_status_brooks_games_for_date import update_brooks_games_for_date_list
from vigorish.status.update_status_brooks_pitch_logs import (
    update_status_brooks_pitch_logs_for_game_list,
)
from vigorish.status.update_status_brooks_pitchfx import update_status_brooks_pitchfx_log_list
from vigorish.tasks.add_to_database import AddToDatabaseTask
from vigorish.tasks.patch_invalid_pfx import PatchInvalidPitchFxTask
from vigorish.util.dt_format_strings import DATE_ONLY_2, DATE_ONLY_TABLE_ID
from vigorish.util.regex import PITCH_APP_REGEX
from vigorish.util.result import Result

DATA_SETS = [DataSet.BBREF_GAMES_FOR_DATE, DataSet.BBREF_BOXSCORES]


class AllTasksforGameDate:
    def __init__(self, app: Vigorish, config: TaskConfigSettings):
        self.app = app
        self.db_session = app.db_session
        self.scraped_data = app.scraped_data
        self.config = config
        self.spinner = None

    @property
    def game_date_str(self):
        return self.game_date.strftime(DATE_ONLY_2) if self.game_date else ""

    @cached_property
    def bbref_game_ids(self):
        bbref_games_for_date = self.scraped_data.get_scraped_data(DataSet.BBREF_GAMES_FOR_DATE, self.game_date)
        return bbref_games_for_date.all_bbref_game_ids if bbref_games_for_date else []

    @cached_property
    def bb_game_ids(self):
        bb_games_for_date = self.scraped_data.get_scraped_data(DataSet.BROOKS_GAMES_FOR_DATE, self.game_date)
        return bb_games_for_date.all_bb_game_ids if bb_games_for_date else []

    @cached_property
    def pitch_app_ids(self):
        bb_games_for_date = self.scraped_data.get_scraped_data(DataSet.BROOKS_GAMES_FOR_DATE, self.game_date)
        return bb_games_for_date.all_pitch_app_ids_for_date if bb_games_for_date else []

    def execute(self, game_date: datetime):
        self.game_date = game_date
        self.year = game_date.year

        return (
            self.reset_scrape_status_for_date()
            .on_success(self.remove_game_data_from_db_for_date)
            .on_success(self.remove_scraped_html)
            .on_success(self.scrape_bbref_data)
            .on_success(self.scrape_mlb_api_data)
            .on_success(self.import_scraped_data)
            .on_success(self.combine_game_data)
            .on_success(self.add_combined_data_to_database)
        )

    def reset_scrape_status_for_date(self):
        if not self.config.reset_db_scrape_status:
            return Result.Ok()
        self._update_heading(f"Removing Data for {self.game_date_str} from Database")
        date_id = self.game_date.strftime(DATE_ONLY_TABLE_ID)
        self.removed_pa_status = (
            self.db_session.query(db.PitchAppScrapeStatus).filter_by(scrape_status_date_id=date_id).delete()
        )
        self.db_session.commit()
        self.removed_game_status = (
            self.db_session.query(db.GameScrapeStatus).filter_by(scrape_status_date_id=date_id).delete()
        )
        self.db_session.commit()
        date_status = db.DateScrapeStatus.find_by_date(self.db_session, self.game_date)
        date_status.scraped_daily_dash_bbref = 0
        date_status.scraped_daily_dash_brooks = 0
        date_status.game_count_bbref = 0
        date_status.game_count_brooks = 0
        self.db_session.commit()
        return Result.Ok()

    def remove_game_data_from_db_for_date(self):
        if not self.config.remove_db_game_data:
            return Result.Ok()
        self._update_heading(f"Removing Data for {self.game_date_str} from Database")
        date_id = self.game_date.strftime(DATE_ONLY_TABLE_ID)
        self.removed_pfx = self.db_session.query(db.PitchFx).filter_by(date_id=date_id).delete()
        self.db_session.commit()
        self.removed_pitchstats = self.db_session.query(db.PitchStats).filter_by(date_id=date_id).delete()
        self.db_session.commit()
        self.removed_batstats = self.db_session.query(db.BatStats).filter_by(date_id=date_id).delete()
        self.db_session.commit()
        return Result.Ok()

    def remove_scraped_html(self):
        self.removed_bbref_html = 0
        for data_set, remove_html in self.config.rescrape_bbref_html.items():
            if not remove_html:
                continue
            self._update_heading(f"Removing Scraped HTML for {DATA_SET_TO_NAME_MAP[data_set]}")
            file_regex = re.compile(f"{self.game_date.strftime(DATE_ONLY_TABLE_ID)}")
            html_folder = self.app.get_current_setting("HTML_LOCAL_FOLDER_PATH", data_set, self.year)
            html_for_date = filter(file_regex.search, os.listdir(html_folder))
            for f in html_for_date:
                self.removed_bbref_html += 1
                Path(html_folder).joinpath(f).unlink()
        return Result.Ok()

    def scrape_bbref_data(self):
        for data_set, scrape_setting in self.config.parse_bbref_html.items():
            self.app.config.change_setting("SCRAPE_CONDITION", data_set, scrape_setting)
        self.app.config.change_setting("STATUS_REPORT", DataSet.ALL, StatusReport.NONE)
        scrape_job = self.app.create_scrape_job(DATA_SETS, self.game_date, self.game_date, "").value
        job_runner = JobRunner(app=self.app, db_job=scrape_job)
        return job_runner.execute()

    def scrape_mlb_api_data(self):
        self._update_heading("Scraping MLB API Data")
        season = db.Season.find_by_year(self.db_session, self.year)
        self._create_spinner(f"Scraping MLB API Data for {self.game_date_str}...")
        result = scrape_mlb_api_data_for_date(
            self.app,
            season,
            self.game_date,
            0,
            self.spinner,
            overwrite_games_for_date=self.config.rescrape_mlb_api[DataSet.BROOKS_GAMES_FOR_DATE],
            overwrite_pfx_data_for_date=self.config.rescrape_mlb_api[DataSet.BROOKS_PITCH_LOGS],
        )
        if result.failure:
            self._destroy_spinner()
            return result
        self._update_heading("Parsing MLB API Data")
        self._update_spinner("Parsing MLB API Data and saving to JSON files...")
        result = convert_mlb_api_data_for_date(
            self.app,
            self.game_date,
            overwrite_games_for_date=self.config.always_parse_mlb_api[DataSet.BROOKS_GAMES_FOR_DATE],
            overwrite_pfx_data_for_date=self.config.always_parse_mlb_api[DataSet.BROOKS_PITCH_LOGS],
        )
        if result.failure:
            self._destroy_spinner()
            return result
        self._destroy_spinner()
        return Result.Ok()

    def import_scraped_data(self):
        self._update_heading("Updating Game/Pitch App Scrape Status")
        self._create_spinner(f"Importing BBRef games for date for {self.game_date.strftime(DATE_ONLY_2)}...")
        result = update_bbref_games_for_date_list(self.scraped_data, self.db_session, [self.game_date])
        if result.failure:
            self._destroy_spinner()
            return result
        self.db_session.commit()
        self._update_spinner(f"Importing Brooks games for date for {self.game_date.strftime(DATE_ONLY_2)}...")
        result = update_brooks_games_for_date_list(self.scraped_data, self.db_session, [self.game_date])
        if result.failure:
            self._destroy_spinner()
            return result
        self.db_session.commit()
        self._update_spinner(f"Importing BBRef boxscores for date {self.game_date.strftime(DATE_ONLY_2)}...")
        result = update_status_bbref_boxscore_list(self.scraped_data, self.db_session, self.bbref_game_ids)
        if result.failure:
            self._destroy_spinner()
            return result
        self.db_session.commit()
        self._update_spinner(f"Importing Brooks pitch logs for date {self.game_date.strftime(DATE_ONLY_2)}...")
        result = update_status_brooks_pitch_logs_for_game_list(self.scraped_data, self.db_session, self.bb_game_ids)
        if result.failure:
            self._destroy_spinner()
            return result
        self.db_session.commit()
        self._update_spinner(f"Importing Brooks PitchFX logs for date {self.game_date.strftime(DATE_ONLY_2)}...")
        result = update_status_brooks_pitchfx_log_list(self.scraped_data, self.db_session, self.pitch_app_ids)
        if result.failure:
            result = self.check_for_missing_pitch_app_ids(result)
        if result.failure:
            self._destroy_spinner()
            return result
        self.db_session.commit()
        self._destroy_spinner()
        return Result.Ok()

    def check_for_missing_pitch_app_ids(self, result):
        for match in PITCH_APP_REGEX.finditer(result.error):
            pitch_app_id = match.group()
            pitch_app_status = db.PitchAppScrapeStatus.find_by_pitch_app_id(self.db_session, pitch_app_id)
            if not pitch_app_status:
                return result
            if pitch_app_status.scraped_pitchfx and pitch_app_status.no_pitchfx_data:
                continue
            return result
        return Result.Ok()

    def combine_game_data(self):
        self.app.config.change_setting("SCRAPED_DATA_COMBINE_CONDITION", DataSet.ALL, self.config.combine_game_data)
        combine_task = CombineScrapedData(self.app)
        (invalid_pfx_game_ids, pfx_error_game_ids) = combine_task.launch_no_prompts(self.game_date.date())
        if pfx_error_game_ids:
            raise ValueError(f"Unfixable PitchFX data errors found! (Game IDs: {pfx_error_game_ids})")
        if invalid_pfx_game_ids:
            result = self.patch_games_with_invalid_pfx_data(invalid_pfx_game_ids)
            if result.failure:
                return result
        return Result.Ok()

    def patch_games_with_invalid_pfx_data(self, invalid_pfx_game_ids):
        self._update_heading("Patching Invalid PitchFx Data")
        self._create_spinner(
            f"Attempting to patch invalid PitchFx data for {invalid_pfx_game_ids[0]} "
            f"(0/{len(invalid_pfx_game_ids)} Games)..."
        )
        for i, game_id in enumerate(invalid_pfx_game_ids, start=1):
            self._update_spinner(
                f"Attempting to patch invalid PitchFx data for {game_id} ({i}/{len(invalid_pfx_game_ids)} Games)..."
            )
            patch_task = PatchInvalidPitchFxTask(self.app)
            result = patch_task.execute(game_id, no_prompts=True)
            if result.failure:
                self._destroy_spinner()
                return result
        self._destroy_spinner()
        return Result.Ok()

    def add_combined_data_to_database(self):
        self._update_heading(f"Adding Game Data for {self.game_date_str} to Database")
        self._create_spinner("Adding player pitch/bat data to database...")
        add_to_db_task = AddToDatabaseTask(self.app)
        add_to_db_task.add_data_for_games(self.year, self.bbref_game_ids)
        self._destroy_spinner()
        return Result.Ok()

    def _update_heading(self, message):
        subprocess.run(["clear"])
        print_heading(message, fg="bright_magenta")

    def _create_spinner(self, message):
        self.spinner = Halo(spinner=get_random_dots_spinner(), color=get_random_cli_color())
        self._update_spinner(message)
        self.spinner.start()

    def _update_spinner(self, message):
        self.spinner.text = message

    def _destroy_spinner(self):
        self.spinner.stop()
        self.spinner.clear()
        self.spinner = None
