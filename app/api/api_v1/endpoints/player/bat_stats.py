from dataclasses import asdict
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import CombinedBatStatsSchema
from app.schema_prep import convert_team_stats

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
    player_bat_stats = [asdict(s) for s in bat_stats]
    return convert_team_stats(app.db_session, player_bat_stats)


@router.get("/by_team", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_team_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_team_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_bat_stats = [asdict(s) for s in bat_stats]
    return convert_team_stats(app.db_session, player_bat_stats)


@router.get("/by_team_by_year", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_team_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_team_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_bat_stats = [asdict(s) for s in bat_stats]
    return convert_team_stats(app.db_session, player_bat_stats)


@router.get("/by_opp_team", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_opp_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_bat_stats = [asdict(s) for s in bat_stats]
    return convert_team_stats(app.db_session, player_bat_stats)


@router.get("/by_opp_team_by_year", response_model=List[CombinedBatStatsSchema])
def get_bat_stats_by_opp_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_bat_stats = [asdict(s) for s in bat_stats]
    return convert_team_stats(app.db_session, player_bat_stats)
