from datetime import date, datetime
from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from vigorish.app import Vigorish
from vigorish.data.game_data import GameData
from vigorish.data.player_data import PlayerData
from vigorish.database import DateScrapeStatus, Player, Season, Team
from vigorish.util.exceptions import ScrapedDataException, UnknownPlayerException


def get_player(mlb_id: int, app: Vigorish):
    return Player.find_by_mlb_id(app.db_session, mlb_id)


def get_team(team_id_br: str, year: int, app: Vigorish):
    return Team.find_by_team_id_and_year(app.db_session, team_id_br, year)


def get_all_game_ids_for_date(game_date: Union[date, datetime], app: Vigorish):
    return DateScrapeStatus.get_all_bbref_game_ids_for_date(app.db_session, game_date)


def get_all_dates_in_season(year: int, app: Vigorish):
    season = Season.find_by_year(app.db_session, year)
    return season.get_date_range() if season else []


def get_game_data(bbref_game_id: str, app: Vigorish):
    try:
        return GameData(app, bbref_game_id)
    except ScrapedDataException as ex:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=repr(ex))


def get_player_data(player_mlb_id: int, app: Vigorish):
    try:
        return PlayerData(app, player_mlb_id)
    except UnknownPlayerException as ex:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=repr(ex))
