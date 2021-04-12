from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.util.dt_format_strings import DATE_ONLY
from vigorish.database import Season, Team

from app.api.dependencies import MLBGameDate, MLBSeason
from app.core import crud
from app.core.cache import cache
from app.core.database import get_vig_app
from app.schema_prep import convert_scoreboard_data, convert_season_to_dict
from app.schemas import ScoreboardSchema, SeasonSchema, TeamLeagueStandings


router = APIRouter()


@router.get("", response_model=SeasonSchema)
@cache()
def get_season(season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)):
    season = Season.find_by_year(app.db_session, season.year)
    if not season:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return season


@router.get("/all", response_model=List[SeasonSchema])
@cache()
def get_all_regular_seasons(app: Vigorish = Depends(get_vig_app)):
    all_mlb_seasons = Season.get_all_regular_seasons(app.db_session)
    if not all_mlb_seasons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return list(map(convert_season_to_dict, filter(lambda x: x.year > 2016 and x.year < 2020, all_mlb_seasons)))


@router.get("/all_dates")
@cache()
def get_all_dates_in_season(season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)):
    all_dates = crud.get_all_dates_in_season(season.year, app)
    if not all_dates:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return [dt.strftime(DATE_ONLY) for dt in all_dates]


@router.get("/standings", response_model=TeamLeagueStandings)
@cache()
def get_regular_season_standings(season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)):
    all_teams = [team.as_dict() for team in Team.get_all_teams_for_season(app.db_session, season.year)]
    return {
        "al": {
            "w": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "W", all_teams), key=lambda x: x["losses"]
            ),
            "c": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "C", all_teams), key=lambda x: x["losses"]
            ),
            "e": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "E", all_teams), key=lambda x: x["losses"]
            ),
        },
        "nl": {
            "w": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "W", all_teams), key=lambda x: x["losses"]
            ),
            "c": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "C", all_teams), key=lambda x: x["losses"]
            ),
            "e": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "E", all_teams), key=lambda x: x["losses"]
            ),
        },
    }


@router.get("/game_ids")
@cache()
def get_all_game_ids_for_date(game_date: MLBGameDate = Depends(), app: Vigorish = Depends(get_vig_app)):
    game_ids = crud.get_all_game_ids_for_date(game_date.date, app)
    if not game_ids:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return game_ids


@router.get("/scoreboard", response_model=ScoreboardSchema)
@cache()
def get_scoreboard_for_date(game_date: MLBGameDate = Depends(), app: Vigorish = Depends(get_vig_app)):
    games_for_date = app.get_scoreboard_data_for_date(game_date.date)
    scoreboard = {"season": game_date.season, "games_for_date": games_for_date}
    return convert_scoreboard_data(scoreboard)
