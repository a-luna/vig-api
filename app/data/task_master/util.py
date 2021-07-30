import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dateutil import parser, tz

from vigorish.config.project_paths import ROOT_FOLDER

MLB_JSON_FOLDER_NAME = "mlb_api_json_storage"
MLB_JSON_FOLDER_PATH = (
    ROOT_FOLDER.joinpath(MLB_JSON_FOLDER_NAME)
    if os.environ["ENV"] == "DEV"
    else Path(__file__).parent.parent.joinpath(MLB_JSON_FOLDER_NAME)
)
TZ_NAME = "America/New_York"
TZ_NEW_YORK = tz.gettz(TZ_NAME)

TEAM_NAME_MAP = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago White Sox": "CHA",
    "Chicago Cubs": "CHN",
    "Cincinnati Reds": "CIN",
    "Cleveland Indians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KCA",
    "Los Angeles Angels of Anaheim": "ANA",
    "Los Angeles Angels": "ANA",
    "Los Angeles Dodgers": "LAN",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Yankees": "NYA",
    "New York Mets": "NYN",
    "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SDN",
    "Seattle Mariners": "SEA",
    "San Francisco Giants": "SFN",
    "St. Louis Cardinals": "SLN",
    "Tampa Bay Rays": "TBA",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WAS",
}

PITCH_CODE_MAP = {
    "C": "S",
    "S": "S",
    "*S": "S",
    "F": "S",
    "B": "B",
    "*B": "B",
    "X": "X",
    "T": "S",
    "K": "S",
    "I": "B",
    "H": "B",
    "L": "S",
    "M": "S",
    "N": "Z",
    "O": "S",
    "P": "B",
    "Q": "S",
    "R": "S",
    "U": "Z",
    "V": "B",
    "Y": "X",
    "1": "Z",
    "2": "Z",
    "3": "Z",
    ">": "Z",
    "+": "Z",
    "*": "Z",
    ".": "Z",
}


def create_bb_game_id(game_date: datetime, game_feed: Dict) -> str:
    away_team_id_bb = game_feed["gameData"]["teams"]["away"]["teamCode"]
    home_team_id_bb = game_feed["gameData"]["teams"]["home"]["teamCode"]
    game_number = game_feed["gameData"]["game"]["gameNumber"]
    return (
        f"gid_{game_date.year}_{game_date.month:02d}_{game_date.day:02d}_"
        f"{away_team_id_bb}mlb_{home_team_id_bb}mlb_{game_number}"
    )


def get_mlb_game_feed(game_date: datetime, bbref_game_id: str) -> Dict:
    game_feed_folder = MLB_JSON_FOLDER_PATH.joinpath(game_date.year).joinpath("game_feeds")
    game_feed_folder.mkdir(parents=True, exist_ok=True)
    game_feed_json = game_feed_folder.joinpath(f"{bbref_game_id}.json")
    if not game_feed_json.exists():
        raise FileNotFoundError
    return json.loads(game_feed_json.read_text())


def get_mlb_ids_for_all_pitchers(game_feed: Dict) -> List[int]:
    away_team_ids = game_feed["liveData"]["boxscore"]["teams"]["away"]["pitchers"]
    home_team_ids = game_feed["liveData"]["boxscore"]["teams"]["home"]["pitchers"]
    return away_team_ids + home_team_ids


def get_game_start_time(game_feed: Dict) -> datetime:
    game_start_str = game_feed["gameData"]["datetime"]["dateTime"]
    return parser.parse(game_start_str).astimezone(TZ_NEW_YORK)


def get_bb_pitch_log_url(game_date: datetime, mlb_game_id: int, mlb_player_id: int) -> str:
    return (
        "https://www.brooksbaseball.net/pfxVB/pfx.php?s_type=2&sp_type=1&batterX=0"
        f"&year={game_date.year}"
        f"&month={str(game_date.month).zfill(2)}"
        f"&day={str(game_date.day).zfill(2)}"
        f"&pitchSel={mlb_player_id}"
        f"&game={mlb_game_id}"
        f"&prevGame={mlb_game_id}"
        f"&prevDate={str(game_date.month).zfill(2)}{str(game_date.day).zfill(2)}"
    )
