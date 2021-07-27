import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pformat
from random import randint
from typing import Union

import requests
from halo import Halo

import vigorish.database as db
from task_master.util import MLB_JSON_FOLDER_PATH
from vigorish.app import Vigorish
from vigorish.cli.components import get_random_cli_color, get_random_dots_spinner
from vigorish.constants import TEAM_NAME_MAP
from vigorish.enums import DataSet
from vigorish.models.season import Season
from vigorish.util.datetime_util import format_timedelta_str
from vigorish.util.dt_format_strings import DATE_ONLY_TABLE_ID, DATE_ONLY_2
from vigorish.util.result import Result

MLB_API_URL_ROOT = "https://statsapi.mlb.com"
MLB_SCHEDULE_API_URL = f"{MLB_API_URL_ROOT}/api/v1/schedule?language=en&sportId=1&date="
BATCH_SIZE = 200
TEN_MINUTES = 10 * 60
FIFTEEN_MINUTES = 15 * 60


def scrape_mlb_api_data_for_season(app: Vigorish, year: int, scrape_count: int, overwrite=False) -> int:
    season = db.Season.find_by_year(app.db_session, year)
    date_range = season.get_date_range()
    spinner = Halo(spinner=get_random_dots_spinner(), color=get_random_cli_color())
    spinner.text = f"0% Complete 0/{len(date_range)} Days ({season.start_date.strftime(DATE_ONLY_2)})..."
    spinner.start()
    result = None
    for i, game_date in enumerate(date_range, start=1):
        result = scrape_mlb_api_data_for_date(app, season, game_date, scrape_count, overwrite)
        if result.failure:
            break
        scrape_count = result.value
        percent_complete = i / float(len(date_range))
        game_date_str = game_date.strftime(DATE_ONLY_2)
        spinner.text = f"{percent_complete:.0%} {i}/{len(date_range)} Days ({game_date_str})..."

    if result.success:
        spinner.succeed("Successfully scraped all game feeds!")
    else:
        spinner.fail("Error occurred!")
        print(result.error)
    return scrape_count


def scrape_mlb_api_data_for_date(
    app: Vigorish,
    season: Season,
    game_date: datetime,
    scrape_count: int,
    spinner: Halo,
    overwrite_games_for_date=False,
    overwrite_pfx_data_for_date=False,
) -> Result:
    json_for_date = get_json_filepath_for_date(game_date)
    if overwrite_games_for_date or not json_for_date.exists():
        scrape_game_schedule(game_date, json_for_date, scrape_count, spinner)
    games_for_date = json.loads(json_for_date.read_text())
    if games_for_date["totalGames"] == 0:
        return Result.Ok(scrape_count)
    if season.is_this_the_asg_date(app.db_session, game_date):
        return Result.Ok(scrape_count)
    games = games_for_date["dates"][0]["games"]
    scraped_game_ids = []
    for game in games:
        bbref_game_id = scrape_game_feed(game, game_date, scrape_count, spinner, overwrite_pfx_data_for_date)
        if bbref_game_id:
            scraped_game_ids.append(bbref_game_id)

    return verify_scraped_game_ids(app, game_date, scraped_game_ids, scrape_count)


def get_json_filepath_for_date(game_date):
    game_schedule_folder = Path(f"{MLB_JSON_FOLDER_PATH}/{game_date.year}/schedule")
    game_schedule_folder.mkdir(parents=True, exist_ok=True)
    file_name = f"{game_date.strftime(DATE_ONLY_TABLE_ID)}.json"
    return game_schedule_folder.joinpath(file_name)


def scrape_game_schedule(game_date, json_for_date, scrape_count, spinner) -> Result:
    url = f"{MLB_SCHEDULE_API_URL}{game_date.strftime(DATE_ONLY_2)}"
    response = requests.get(url)
    if response.status_code >= 400:
        error = f"Request for games scheduled on {game_date.strftime(DATE_ONLY_2)} was unsuccessful!"
        return Result.Fail(error)
    resp_json = response.json()
    json_for_date.write_text(json.dumps(resp_json, indent=2, sort_keys=False))
    scrape_count += 1
    if scrape_count >= BATCH_SIZE:
        batch_scrape_delay(spinner)
        scrape_count = 0
    return Result.Ok()


def scrape_game_feed(game, game_date, scrape_count, spinner, overwrite_pfx_data_for_date=False) -> Union[None, str]:
    game_state = game["status"]["codedGameState"]
    game_state_is_invalid = (
        game_state in ["C", "U"]
        or (game_state != "F" and "rescheduledFrom" not in game)
        or "resumedFrom" in game
        or "rescheduleDate" in game
    )
    if game_state_is_invalid:
        return None
    bbref_game_id = get_game_id(game, game_date)
    game_feed_json = get_json_filepath_for_game(bbref_game_id, game_date)
    if not overwrite_pfx_data_for_date and game_feed_json.exists():
        return bbref_game_id
    url = f'{MLB_API_URL_ROOT}{game["link"]}'
    response = requests.get(url)
    if response.status_code > 200:
        return None
    resp_json = response.json()
    game_feed_json.write_text(json.dumps(resp_json, indent=2, sort_keys=False))
    sleep = randint(2500, 6000) / float(1000)
    time.sleep(sleep)
    scrape_count += 1
    if scrape_count >= BATCH_SIZE:
        batch_scrape_delay(spinner)
        scrape_count = 0
    return bbref_game_id


def get_json_filepath_for_game(bbref_game_id, game_date):
    game_feed_folder = Path(f"{MLB_JSON_FOLDER_PATH}/{game_date.year}/game_feeds")
    game_feed_folder.mkdir(parents=True, exist_ok=True)
    file_name = f"{bbref_game_id}.json"
    return game_feed_folder.joinpath(file_name)


def get_game_id(game, game_date) -> str:
    home_team = game["teams"]["home"]["team"]["name"]
    if game["reverseHomeAwayStatus"]:
        home_team = game["teams"]["away"]["team"]["name"]
    home_team_id = TEAM_NAME_MAP.get(home_team)
    game_number = 0
    if game["doubleHeader"] != "N":
        game_number = game["gameNumber"]
    return f"{home_team_id}{game_date.strftime(DATE_ONLY_TABLE_ID)}{game_number}"


def batch_scrape_delay(spinner):
    sleep = randint(TEN_MINUTES, FIFTEEN_MINUTES)
    while sleep:
        td = timedelta(seconds=sleep)
        spinner.text = f"Waiting {format_timedelta_str(td)} until next batch..."
        time.sleep(1)
        sleep -= 1


def verify_scraped_game_ids(app, game_date, scraped_game_ids, scrape_count) -> Result:
    bbref_games_for_date = app.scraped_data.get_scraped_data(DataSet.BBREF_GAMES_FOR_DATE, game_date)
    bbref_game_ids = bbref_games_for_date.all_bbref_game_ids
    wrong_mlb_game_ids = list(set(scraped_game_ids) - set(bbref_game_ids))
    missing_bbref_game_ids = list(set(bbref_game_ids) - set(scraped_game_ids))
    if not wrong_mlb_game_ids and not missing_bbref_game_ids:
        return Result.Ok(scrape_count)
    error_dict = {}
    if wrong_mlb_game_ids:
        error_dict["wrong_mlb_game_ids"] = wrong_mlb_game_ids
    if missing_bbref_game_ids:
        error_dict["missing_bbref_game_ids"] = missing_bbref_game_ids
    return Result.Fail(pformat(error_dict))
