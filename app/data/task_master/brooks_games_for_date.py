from datetime import datetime
from typing import Dict, List

from dacite import from_dict

from task_master.util import (
    TZ_NAME,
    create_bb_game_id,
    get_bb_pitch_log_url,
    get_game_start_time,
    get_mlb_game_feed,
    get_mlb_ids_for_all_pitchers,
)
from vigorish.app import Vigorish
from vigorish.enums import DataSet
from vigorish.scrape.brooks_games_for_date.models.games_for_date import BrooksGamesForDate
from vigorish.util.dt_format_strings import DATE_ONLY


def get_brooks_games_for_date(app: Vigorish, game_date: datetime) -> BrooksGamesForDate:
    bbref_game_ids = get_bbref_game_ids_for_date(app, game_date)
    games_for_date = {
        "dashboard_url": get_bb_dashboard_url(game_date),
        "game_date": game_date,
        "game_date_str": game_date.strftime(DATE_ONLY),
        "game_count": str(len(bbref_game_ids)),
        "games": [get_brooks_game_info(game_date, game_id) for game_id in bbref_game_ids],
    }
    return from_dict(data_class=BrooksGamesForDate, data=games_for_date)


def get_bbref_game_ids_for_date(app: Vigorish, game_date: datetime) -> List[str]:
    bbref_games_for_date = app.scraped_data.get_scraped_data(DataSet.BBREF_GAMES_FOR_DATE, game_date)
    return bbref_games_for_date.all_bbref_game_ids


def get_bb_dashboard_url(game_date: datetime) -> str:
    return f"http://www.brooksbaseball.net/dashboard.php?dts={game_date.month}/{game_date.day}/{game_date.year}"


def get_brooks_game_info(game_date: datetime, bbref_game_id: str) -> Dict:
    game_feed = get_mlb_game_feed(game_date, bbref_game_id)
    game_start_time = get_game_start_time(game_feed)
    mlb_game_id = game_feed["gamePk"]
    mlb_pitcher_ids = get_mlb_ids_for_all_pitchers(game_feed)
    pitch_app_url_dict = {
        str(mlb_id): get_bb_pitch_log_url(game_date, mlb_game_id, mlb_id) for mlb_id in mlb_pitcher_ids
    }
    return {
        "might_be_postponed": False,
        "game_date_year": str(game_start_time.year),
        "game_date_month": str(game_start_time.month),
        "game_date_day": str(game_start_time.day),
        "game_time_hour": str(game_start_time.hour),
        "game_time_minute": str(game_start_time.minute),
        "time_zone_name": TZ_NAME,
        "mlb_game_id": str(mlb_game_id),
        "bb_game_id": create_bb_game_id(game_date, game_feed),
        "bbref_game_id": str(bbref_game_id),
        "away_team_id_bb": game_feed["gameData"]["teams"]["away"]["teamCode"].upper(),
        "home_team_id_bb": game_feed["gameData"]["teams"]["home"]["teamCode"].upper(),
        "game_number_this_day": game_feed["gameData"]["game"]["gameNumber"],
        "pitcher_appearance_count": len(mlb_pitcher_ids),
        "pitcher_appearance_dict": pitch_app_url_dict,
    }
