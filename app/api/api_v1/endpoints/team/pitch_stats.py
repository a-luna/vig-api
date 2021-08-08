from dataclasses import asdict
from http import HTTPStatus
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish
from vigorish.enums import TeamID

from app.api.dependencies import MLBSeason, TeamParameters
from app.core.database import get_vig_app
from app.schemas import CombinedPitchStatsSchema
from app.schema_prep import convert_team_stats

router = APIRouter()


@router.get("/", response_model=CombinedPitchStatsSchema)
def get_pitch_stats_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/sp", response_model=CombinedPitchStatsSchema)
@cache()
def get_pitch_stats_for_sp_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_sp_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/rp", response_model=CombinedPitchStatsSchema)
def get_pitch_stats_for_rp_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_rp_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return asdict(pitch_stats)


@router.get("/by_year", response_model=Dict[int, CombinedPitchStatsSchema])
def get_pitch_stats_by_year_for_team(
    request: Request, response: Response, team_id: TeamID, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/sp/by_year", response_model=Dict[int, CombinedPitchStatsSchema])
def get_pitch_stats_for_sp_by_year_for_team(
    request: Request, response: Response, team_id: TeamID, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_sp_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/rp/by_year", response_model=Dict[int, CombinedPitchStatsSchema])
def get_pitch_stats_for_rp_by_year_for_team(
    request: Request, response: Response, team_id: TeamID, app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_rp_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/by_player", response_model=List[CombinedPitchStatsSchema])
def get_pitch_stats_by_player_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/sp/by_player", response_model=List[CombinedPitchStatsSchema])
def get_pitch_stats_for_sp_by_player_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_sp_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/rp/by_player", response_model=List[CombinedPitchStatsSchema])
def get_pitch_stats_for_rp_by_player_for_team(
    request: Request, response: Response, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_rp_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    player_pitch_stats = [asdict(stats) for stats in pitch_stats]
    return convert_team_stats(app.db_session, player_pitch_stats)


@router.get("/all_teams", response_model=Dict[str, CombinedPitchStatsSchema])
def get_pitch_stats_for_season_for_all_teams(
    request: Request, response: Response, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    all_teams = {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}
    return convert_team_stats(app.db_session, all_teams)


@router.get("/sp/all_teams", response_model=Dict[str, CombinedPitchStatsSchema])
def get_pitch_stats_for_sp_for_season_for_all_teams(
    request: Request, response: Response, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_sp_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    all_teams = {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}
    return convert_team_stats(app.db_session, all_teams)


@router.get("/rp/all_teams", response_model=Dict[str, CombinedPitchStatsSchema])
def get_pitch_stats_for_rp_for_season_for_all_teams(
    request: Request, response: Response, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_rp_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    all_teams = {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}
    return convert_team_stats(app.db_session, all_teams)
