from dataclasses import asdict
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import CombinedBatStatsSchema, CareerBatStatsSchema
from app.schema_prep import (
    convert_career_bat_stats,
    convert_player_team_stats,
    calc_season_bat_stats_for_player,
    calc_career_bat_stats_for_player,
)

router = APIRouter()


@router.get("/", response_model=CombinedBatStatsSchema)
def get_bat_stats_for_career_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_for_career_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(bat_stats)


@router.get("/by_year", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return [convert_player_team_stats(asdict(s)) for s in bat_stats]


@router.get("/by_team", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_team_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_team_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return [convert_player_team_stats(asdict(s)) for s in bat_stats]


@router.get("/by_team_by_year", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_team_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_team_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return [convert_player_team_stats(asdict(s)) for s in bat_stats]


@router.get("/career_stats", response_model=CareerBatStatsSchema)
@cache()
def get_career_bat_stats_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats_for_career = app.scraped_data.get_bat_stats_for_career_for_player(mlb_id)
    bat_stats_by_year = app.scraped_data.get_bat_stats_by_year_for_player(mlb_id)
    bat_stats_by_team = app.scraped_data.get_bat_stats_by_team_for_player(mlb_id)
    bat_stats_by_team_by_year = app.scraped_data.get_bat_stats_by_team_by_year_for_player(mlb_id)
    if not bat_stats_for_career or not bat_stats_by_year or not bat_stats_by_team or not bat_stats_by_team_by_year:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return {
        "career": convert_career_bat_stats(bat_stats_for_career, len(bat_stats_by_year)),
        "by_team": calc_career_bat_stats_for_player(app, mlb_id, bat_stats_by_team, bat_stats_by_team_by_year),
        "by_team_by_year": calc_season_bat_stats_for_player(app, mlb_id, bat_stats_by_year, bat_stats_by_team_by_year),
    }


@router.get("/by_opp_team", response_model=List[CombinedBatStatsSchema])
@cache()
def get_bat_stats_by_opp_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return [convert_player_team_stats(asdict(s)) for s in bat_stats]


@router.get("/by_opp_team_by_year", response_model=List[CombinedBatStatsSchema])
@cache()
def get_bat_stats_by_opp_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return [convert_player_team_stats(asdict(s)) for s in bat_stats]
