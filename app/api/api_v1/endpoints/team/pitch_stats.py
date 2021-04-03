from dataclasses import asdict
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.enums import TeamID

from app.api.dependencies import MLBSeason, TeamParameters
from app.core.database import get_vig_app
from app.schemas import PitchStatsSchema


router = APIRouter()


@router.get("/", response_model=PitchStatsSchema)
def get_pitch_stats_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/sp", response_model=PitchStatsSchema)
def get_pitch_stats_for_sp_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_for_sp_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/rp", response_model=PitchStatsSchema)
def get_pitch_stats_for_rp_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_for_rp_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/by_year", response_model=Dict[int, PitchStatsSchema])
def get_pitch_stats_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/sp/by_year", response_model=Dict[int, PitchStatsSchema])
def get_pitch_stats_for_sp_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_sp_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/rp/by_year", response_model=Dict[int, PitchStatsSchema])
def get_pitch_stats_for_rp_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_rp_by_year_for_team(team_id.name)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(pitch_stats) for year, pitch_stats in pitch_stats_dict.items()}


@router.get("/by_player", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_player_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/sp/by_player", response_model=List[PitchStatsSchema])
def get_pitch_stats_for_sp_by_player_for_team(
    team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_sp_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/rp/by_player", response_model=List[PitchStatsSchema])
def get_pitch_stats_for_rp_by_player_for_team(
    team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats = app.scraped_data.get_pitch_stats_for_rp_by_player_for_team(team_params.team_id, team_params.year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/all_teams", response_model=Dict[str, PitchStatsSchema])
def get_pitch_stats_for_season_for_all_teams(season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}


@router.get("/sp/all_teams", response_model=Dict[str, PitchStatsSchema])
def get_pitch_stats_for_sp_for_season_for_all_teams(
    season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_sp_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}


@router.get("/rp/all_teams", response_model=Dict[str, PitchStatsSchema])
def get_pitch_stats_for_rp_for_season_for_all_teams(
    season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pitch_stats_dict = app.scraped_data.get_pitch_stats_for_rp_for_season_for_all_teams(season.year)
    if not pitch_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {team_id: asdict(pitch_stats) for team_id, pitch_stats in pitch_stats_dict.items()}