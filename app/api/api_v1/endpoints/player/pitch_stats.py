from dataclasses import asdict
from http import HTTPStatus
from typing import List

import vigorish.database as db
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache, cache_one_week
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import CombinedPitchStatsSchema, CareerPitchStatsSchema
from app.schema_prep import (
    convert_team_stats,
    convert_career_bat_stats,
    calc_season_bat_stats_for_player,
    calc_career_bat_stats_for_player,
)

router = APIRouter()


@router.get("/", response_model=CombinedPitchStatsSchema)
@cache_one_week()
def get_pitch_stats_for_career_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_career_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/as_sp", response_model=CombinedPitchStatsSchema)
@cache_one_week()
def get_pitch_stats_as_sp_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_as_sp_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/as_rp", response_model=CombinedPitchStatsSchema)
@cache_one_week()
def get_pitch_stats_as_rp_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_as_rp_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/by_year", response_model=List[CombinedPitchStatsSchema])
@cache_one_week()
def get_pitch_stats_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/by_team", response_model=List[CombinedPitchStatsSchema])
@cache_one_week()
def get_pitch_stats_by_team_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_team_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/by_team_by_year", response_model=List[CombinedPitchStatsSchema])
@cache_one_week()
def get_pitch_stats_by_team_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_team_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/by_opp_team", response_model=List[CombinedPitchStatsSchema])
@cache_one_week()
def get_pitch_stats_by_opp_team_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_opp_team_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/by_opp_team_by_year", response_model=List[CombinedPitchStatsSchema])
@cache_one_week()
def get_pitch_stats_by_opp_team_by_year_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_opp_team_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/career_stats", response_model=CareerPitchStatsSchema)
@cache_one_week()
def get_career_pitch_stats_for_player(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_for_career = app.scraped_data.get_pitch_stats_for_career_for_player(mlb_id)
    pitch_stats_by_year = app.scraped_data.get_pitch_stats_by_year_for_player(mlb_id)
    pitch_stats_by_team = app.scraped_data.get_pitch_stats_by_team_for_player(mlb_id)
    pitch_stats_by_team_by_year = app.scraped_data.get_pitch_stats_by_team_by_year_for_player(mlb_id)
    if (
        not pitch_stats_for_career
        or not pitch_stats_by_year
        or not pitch_stats_by_team
        or not pitch_stats_by_team_by_year
    ):
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return {
        "career": convert_career_bat_stats(pitch_stats_for_career, len(pitch_stats_by_year)),
        "by_team": calc_career_bat_stats_for_player(app, mlb_id, pitch_stats_by_team, pitch_stats_by_team_by_year),
        "by_team_by_year": calc_season_bat_stats_for_player(
            app, mlb_id, pitch_stats_by_year, pitch_stats_by_team_by_year
        ),
    }


@router.get("/pitch_app_ids", response_model=List[str])
@cache()
def get_pitch_app_ids_for_game(request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_id = db.PlayerId.find_by_mlb_id(app.db_session, mlb_id)
    if not player_id:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    pitch_app_status_list = (
        app.db_session.query(db.PitchAppScrapeStatus).filter_by(pitcher_id=player_id.db_player_id).all()
    )
    return [p.pitch_app_id for p in pitch_app_status_list]
