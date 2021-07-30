import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import requests
from halo import Halo

from task_master.id_player_types import define_all_player_team_roles
from task_master.all_tasks_for_date import AllTasksforGameDate
from task_master.task_config_settings import TaskConfigSettings
from vigorish.cli.components.util import get_random_cli_color, get_random_dots_spinner, print_heading
from vigorish.app import Vigorish
from vigorish.cli.menu_items.admin_tasks import UpdatePlayerIdMap
from vigorish.enums import DataSet, ScrapeCondition
from vigorish.util.datetime_util import get_date_range
from vigorish.util.result import Result
from vigorish.util.sys_helpers import hash_all_files_in_folder, run_command

os.environ["INTERACTIVE_MODE"] = "NO"

S3_LOCAL_FOLDER = (
    Path("/Users/aluna/Desktop/s3") if os.environ["ENV"] == "DEV" else Path(__file__).parent.parent.joinpath("s3")
)
S3_BUCKET_NAME = "alunapublic"
S3_DEST_FOLDER = "vig-api"
S3_BUCKET_URL = f"s3://{S3_BUCKET_NAME}/{S3_DEST_FOLDER}"


class TaskMaster:
    def __init__(self, app: Vigorish, config: TaskConfigSettings):
        self.app = app
        self.db_session = app.db_session
        self.config = config

    def execute(self):
        return (
            self.update_id_map()
            .on_success(self.update_player_team_roles)
            .on_success(self.run_all_tasks_for_date_range)
            .on_success(self.create_vig_db_zip_file)
            .on_success(self.create_combined_data_zip_file)
            .on_success(self.upload_zip_files_to_s3)
            .on_success(self.restart_dokku_container)
        )

    def update_id_map(self):
        if not self.config.update_id_map:
            return Result.Ok()
        try:
            update_id_map_task = UpdatePlayerIdMap(self.app)
            return update_id_map_task.launch(no_prompts=True)
        except requests.exceptions.SSLError:
            return Result.Ok()

    def update_player_team_roles(self):
        if not self.config.update_player_team_roles:
            return Result.Ok()
        define_all_player_team_roles(self.app)
        return Result.Ok()

    def run_all_tasks_for_date_range(self):
        result = self.get_date_range_to_scrape()
        if result.failure:
            return Result.Ok()
        date_range = result.value
        for game_date in date_range:
            all_tasks = AllTasksforGameDate(self.app, self.config)
            result = all_tasks.execute(game_date)
            if result.failure:
                return result
        return Result.Ok()

    def get_date_range_to_scrape(self):
        start = self.get_scrape_start_date()
        end = self.get_scrape_end_date()
        if start > end:
            return Result.Fail("All possible game data has been scraped.")
        return Result.Ok(get_date_range(start, end))

    def get_scrape_start_date(self):
        most_recent = self.app.get_most_recent_scraped_date()
        return datetime(most_recent.year, most_recent.month, most_recent.day + 1)

    def get_scrape_end_date(self):
        now = datetime.utcnow()
        if now.hour >= 10:
            return datetime(now.year, now.month, now.day - 1)
        return datetime(now.year, now.month, now.day - 2)

    def create_vig_db_zip_file(self):
        if not self.config.backup_db:
            return Result.Ok()
        self._update_heading("Compressing SQLite Database File")
        self._create_spinner("Compressing vig.db file...")
        target_filepath = S3_LOCAL_FOLDER.joinpath("vig.db.zip")
        with ZipFile(target_filepath, "w", ZIP_DEFLATED) as zip:
            zip.write(self.app.db_filepath, arcname=f"{S3_LOCAL_FOLDER.name}/{self.app.db_filepath.name}")
        self._destroy_spinner()
        return Result.Ok()

    def create_combined_data_zip_file(self):
        if not self.config.backup_combined_data_json:
            return Result.Ok()
        self._update_heading(f"Compressing Combined Data JSON files for {self.config.mlb_season}")
        self._create_spinner(f"Compressing {self.config.mlb_season} combined data files...")
        source_folder = Path(
            self.app.get_current_setting("COMBINED_DATA_LOCAL_FOLDER_PATH", DataSet.ALL, year=self.config.mlb_season)
        )
        shutil.make_archive(
            base_name=f"{S3_LOCAL_FOLDER}/{self.config.mlb_season}",
            format="zip",
            root_dir=source_folder.parent,
            base_dir=source_folder.name,
        )
        self._destroy_spinner()
        return Result.Ok()

    def upload_zip_files_to_s3(self):
        if not self.config.upload_backup_files_to_s3:
            return Result.Ok()
        hash_all_files_in_folder(S3_LOCAL_FOLDER, create_hash_files=True)
        self._update_heading("Uploading Compressed Files to S3")
        sync_zip_files_command = (
            f'aws s3 sync . {S3_BUCKET_URL} --size-only --exclude "*" --include "2021.zip" --include "vig.db.zip"'
        )
        sync_hash_files_command = (
            f'aws s3 sync . {S3_BUCKET_URL} --exclude "*" --include "2021.zip.md5" --include "vig.db.zip.md5"'
        )
        result = run_command(sync_zip_files_command, cwd=str(S3_LOCAL_FOLDER))
        result = run_command(sync_hash_files_command, cwd=str(S3_LOCAL_FOLDER))
        return result

    def restart_dokku_container(self):
        if not self.config.redeploy_dokku_app:
            return Result.Ok()
        redeploy_app_command = "dokku ps:restart vig-api"
        return run_command(redeploy_app_command)

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


def get_config():
    mlb_season = 2021
    reset_db_scrape_status = False
    remove_db_game_data = False
    update_id_map = True
    update_player_team_roles = False
    rescrape_bbref_html = {
        DataSet.BBREF_GAMES_FOR_DATE: False,
        DataSet.BBREF_BOXSCORES: False,
    }
    parse_bbref_html = {
        DataSet.BBREF_GAMES_FOR_DATE: ScrapeCondition.ONLY_MISSING_DATA,
        DataSet.BBREF_BOXSCORES: ScrapeCondition.ONLY_MISSING_DATA,
    }
    rescrape_mlb_api = {
        DataSet.BROOKS_GAMES_FOR_DATE: False,
        DataSet.BROOKS_PITCH_LOGS: False,
    }
    always_parse_mlb_api = {
        DataSet.BROOKS_GAMES_FOR_DATE: False,
        DataSet.BROOKS_PITCH_LOGS: False,
    }
    combine_game_data = ScrapeCondition.ONLY_MISSING_DATA
    backup_db = True
    backup_combined_data_json = True
    upload_backup_files_to_s3 = True
    restart_dokku_container = False

    config_dict = {
        "mlb_season": mlb_season,
        "reset_db_scrape_status": reset_db_scrape_status,
        "remove_db_game_data": remove_db_game_data,
        "update_id_map": update_id_map,
        "update_player_team_roles": update_player_team_roles,
        "rescrape_bbref_html": rescrape_bbref_html,
        "parse_bbref_html": parse_bbref_html,
        "rescrape_mlb_api": rescrape_mlb_api,
        "always_parse_mlb_api": always_parse_mlb_api,
        "combine_game_data": combine_game_data,
        "backup_db": backup_db,
        "backup_combined_data_json": backup_combined_data_json,
        "upload_backup_files_to_s3": upload_backup_files_to_s3,
        "restart_dokku_container": restart_dokku_container,
    }

    return TaskConfigSettings(**config_dict)


def main():
    app = Vigorish()
    config = get_config()
    if config.backup_db or config.backup_combined_data_json:
        S3_LOCAL_FOLDER.mkdir(parents=True, exist_ok=True)
    task_master = TaskMaster(app, config)
    result = task_master.execute()
    if result.failure:
        print(f"Error occurred!\n{result.error}")
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()
