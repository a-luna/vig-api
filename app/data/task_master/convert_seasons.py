from datetime import datetime
from pathlib import Path

from halo import Halo

from task_master.brooks_games_for_date import get_brooks_games_for_date
from task_master.brooks_pitchfx import PitchFxDataConverter
from vigorish.app import Vigorish
from vigorish.cli.components import get_random_cli_color, get_random_dots_spinner
from vigorish.enums import DataSet
from vigorish.util.dt_format_strings import DATE_ONLY_2
from vigorish.util.regex import BBREF_DAILY_JSON_FILENAME_REGEX_STRICT, BBREF_GAME_ID_REGEX_STRICT
from vigorish.util.result import Result
from vigorish.util.string_helpers import get_game_date_from_bbref_game_id


def convert_mlb_api_data_for_season(app: Vigorish, year: int):
    bbref_games_for_date_folder = app.get_current_setting("JSON_LOCAL_FOLDER_PATH", DataSet.BBREF_GAMES_FOR_DATE, year)
    bbref_games_for_date_json_files = list(Path(bbref_games_for_date_folder).glob("*.json"))
    bbref_games_for_date_json_files.sort(key=lambda x: x.name)
    total_days = len(bbref_games_for_date_json_files)
    percent = 0
    spinner = Halo(spinner=get_random_dots_spinner(), color=get_random_cli_color())
    spinner.text = "0% Complete"
    spinner.start()
    for days_complete, bbref_games_for_date_json in enumerate(bbref_games_for_date_json_files):
        match = BBREF_DAILY_JSON_FILENAME_REGEX_STRICT.search(bbref_games_for_date_json.stem)
        if match:
            groups = match.groupdict()
            game_date = datetime(int(groups["year"]), int(groups["month"]), int(groups["day"]))
            if not brooks_games_for_date_exists(app, game_date):
                convert_mlb_schedule_for_date(app, game_date)
        percent = days_complete / float(total_days)
        game_date_str = game_date.strftime(DATE_ONLY_2) if game_date else "          "
        spinner.text = f"{percent:.0%} Complete {days_complete}/{total_days} Days ({game_date_str})"
    spinner.succeed = "Created all Brooks Games For Date JSON files!"
    spinner.stop()
    spinner.clear()
    spinner = None

    boxscores_folder = app.get_current_setting("JSON_LOCAL_FOLDER_PATH", DataSet.BBREF_BOXSCORES, year)
    boxscore_json_files = list(Path(boxscores_folder).glob("*.json"))
    boxscore_json_files.sort(key=lambda x: x.name)
    total_games = len(boxscore_json_files)
    percent = 0
    spinner = Halo(spinner=get_random_dots_spinner(), color=get_random_cli_color())
    spinner.text = "0% Complete"
    spinner.start()
    for games_complete, boxscore_json in enumerate(boxscore_json_files):
        game_id = boxscore_json.stem
        if BBREF_GAME_ID_REGEX_STRICT.match(game_id) and not brooks_pitch_logs_for_game_exists(app, game_id):
            game_date = get_game_date_from_bbref_game_id(game_id)
            convert_mlb_api_data_for_game(app, game_date, game_id)
        percent = games_complete / float(total_games)
        spinner.text = f"{percent:.0%} Complete {games_complete}/{total_games} Games ({game_id})"
    spinner.succeed = "Created all Brooks Pitch Logs and PitchFX Log JSON files!"
    spinner.stop()
    spinner.clear()
    spinner = None


def bbref_games_for_date_exists(app: Vigorish, game_date: datetime) -> bool:
    bbref_games_for_date = app.scraped_data.get_scraped_data(DataSet.BBREF_GAMES_FOR_DATE, game_date)
    return bbref_games_for_date is not None


def brooks_games_for_date_exists(app: Vigorish, game_date: datetime) -> bool:
    brooks_games_for_date = app.scraped_data.get_scraped_data(DataSet.BROOKS_GAMES_FOR_DATE, game_date)
    return brooks_games_for_date is not None


def brooks_pitch_logs_for_game_exists(app: Vigorish, bbref_game_id: str) -> bool:
    bbref_boxscore = app.scraped_data.get_scraped_data(DataSet.BBREF_BOXSCORES, bbref_game_id)
    pitch_logs_for_game = app.scraped_data.get_scraped_data(DataSet.BROOKS_PITCH_LOGS, bbref_boxscore.bb_game_id)
    return pitch_logs_for_game is not None


def pitchfx_log_for_pitch_app_exists(app: Vigorish, pitch_app_id: str) -> bool:
    pitchfx_log = app.scraped_data.get_scraped_data(DataSet.BROOKS_PITCHFX, pitch_app_id)
    return pitchfx_log is not None


def get_all_bbref_game_ids_for_date(app: Vigorish, game_date: datetime):
    bbref_games_for_date = app.scraped_data.get_scraped_data(DataSet.BBREF_GAMES_FOR_DATE, game_date)
    return bbref_games_for_date.all_bbref_game_ids if bbref_games_for_date else []


def get_all_pitch_app_ids_for_date(app: Vigorish, game_date: datetime):
    bb_games_for_date = app.scraped_data.get_scraped_data(DataSet.BROOKS_GAMES_FOR_DATE, game_date)
    return bb_games_for_date.all_pitch_app_ids_for_date if bb_games_for_date else []


def convert_mlb_api_data_for_date(
    app: Vigorish,
    game_date: datetime,
    overwrite_games_for_date: bool = False,
    overwrite_pfx_data_for_date: bool = False,
) -> Result:
    if overwrite_games_for_date or not brooks_games_for_date_exists(app, game_date):
        convert_mlb_schedule_for_date(app, game_date)
    if overwrite_pfx_data_for_date or not all_pitchfx_logs_for_date_exist(app, game_date):
        return convert_mlb_game_feed_for_date(app, game_date, overwrite_pfx_data_for_date)
    return Result.Ok()


def convert_mlb_schedule_for_date(app: Vigorish, game_date: datetime) -> None:
    games_for_date = get_brooks_games_for_date(app, game_date)
    app.scraped_data.save_json(DataSet.BROOKS_GAMES_FOR_DATE, games_for_date)


def all_pitchfx_logs_for_date_exist(app: Vigorish, game_date: datetime):
    bbref_game_ids = get_all_bbref_game_ids_for_date(app, game_date)
    pitch_app_ids = get_all_pitch_app_ids_for_date(app, game_date)
    all_pitch_logs_exist = all(brooks_pitch_logs_for_game_exists(app, game_id) for game_id in bbref_game_ids)
    all_pitchfx_logs_exist = all(pitchfx_log_for_pitch_app_exists(app, pitch_app_id) for pitch_app_id in pitch_app_ids)
    return all_pitch_logs_exist and all_pitchfx_logs_exist


def convert_mlb_game_feed_for_date(
    app: Vigorish, game_date: datetime, overwrite_pfx_data_for_date: bool = False
) -> Result:
    if not bbref_games_for_date_exists(app, game_date):
        game_date_str = game_date.strftime(DATE_ONLY_2)
        return Result.Fail(f"JSON file for BBRef games for date for {game_date_str} does not exist")
    for game_id in get_all_bbref_game_ids_for_date(app, game_date):
        convert_mlb_api_data_for_game(app, game_date, game_id, overwrite_pfx_data_for_date)
    return Result.Ok()


def convert_mlb_api_data_for_game(
    app: Vigorish, game_date: datetime, bbref_game_id: str, overwrite_pfx_data_for_date: bool = False
):
    pfx_converter = PitchFxDataConverter()
    (pitch_logs_for_game, pfx_logs_for_game) = pfx_converter.get_brooks_pitchfx_logs_for_game(game_date, bbref_game_id)
    if overwrite_pfx_data_for_date or not brooks_pitch_logs_for_game_exists(app, bbref_game_id):
        app.scraped_data.save_json(DataSet.BROOKS_PITCH_LOGS, pitch_logs_for_game)
    for pfx_log in pfx_logs_for_game:
        if overwrite_pfx_data_for_date or not pitchfx_log_for_pitch_app_exists(app, pfx_log.pitch_app_id):
            result = app.scraped_data.save_json(DataSet.BROOKS_PITCHFX, pfx_log)
            if result.failure:
                raise ValueError(result.error)
