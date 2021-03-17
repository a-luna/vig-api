from dataclasses import asdict
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.enums import TeamID, DefensePosition

from app.api.dependencies import BatOrder, MLBSeason, TeamParameters
from app.core.database import get_vig_app
from app.schemas import BatStatsSchema


router = APIRouter()


@router.get("/", response_model=BatStatsSchema)
def get_bat_stats_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(bat_stats)


@router.get("/by_bat_order", response_model=List[BatStatsSchema])
def get_bat_stats_by_bat_order_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_lineup_spot_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/by_position", response_model=List[BatStatsSchema])
def get_bat_stats_by_defpos_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_defpos_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/starters", response_model=BatStatsSchema)
def get_bat_stats_for_starters_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_for_starters_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(bat_stats)


@router.get("/subs", response_model=BatStatsSchema)
def get_bat_stats_for_subs_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_for_subs_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(bat_stats)


@router.get("/by_year", response_model=Dict[int, BatStatsSchema])
def get_bat_stats_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    bat_stats_dict = app.scraped_data.get_bat_stats_by_year_for_team(team_id.name)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/bat_order/by_year", response_model=Dict[int, BatStatsSchema])
def get_bat_stats_for_lineup_spot_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_lineup_spot_by_year_for_team(team_id.name)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/position/by_year", response_model=Dict[int, BatStatsSchema])
def get_bat_stats_for_defpos_by_year_for_team(
    def_position: DefensePosition, team_id: TeamID, app: Vigorish = Depends(get_vig_app)
):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_defpos_by_year_for_team(def_position, team_id.name)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/starters/by_year", response_model=Dict[int, BatStatsSchema])
def get_bat_stats_for_starters_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_starters_by_year_for_team(team_id.name)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/subs/by_year", response_model=Dict[int, BatStatsSchema])
def get_bat_stats_for_subs_by_year_for_team(team_id: TeamID, app: Vigorish = Depends(get_vig_app)):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_subs_by_year_for_team(team_id.name)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/by_player", response_model=List[BatStatsSchema])
def get_bat_stats_by_player_for_team(team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_player_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/bat_order/by_player", response_model=List[BatStatsSchema])
def get_bat_stats_for_lineup_spot_by_player_for_team(
    bat_order: BatOrder = Depends(), team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_for_lineup_spot_by_player_for_team(
        bat_order.number, team_params.team_id, team_params.year
    )
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/position/by_player", response_model=List[BatStatsSchema])
def get_bat_stats_for_defensive_position_by_player_for_team(
    def_position: DefensePosition, team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_for_defpos_by_player_for_team(
        def_position, team_params.team_id, team_params.year
    )
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/starters/by_player", response_model=List[BatStatsSchema])
def get_bat_stats_for_starters_by_player_for_team(
    team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_for_starters_by_player_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/subs/by_player", response_model=List[BatStatsSchema])
def get_bat_stats_for_subs_by_player_for_team(
    team_params: TeamParameters = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats = app.scraped_data.get_bat_stats_for_subs_by_player_for_team(team_params.team_id, team_params.year)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/all_teams", response_model=Dict[str, BatStatsSchema])
def get_bat_stats_for_season_for_all_teams(season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_season_for_all_teams(season.year)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/bat_order/all_teams", response_model=Dict[str, BatStatsSchema])
def get_bat_stats_for_lineup_spot_for_season_for_all_teams(
    bat_order: BatOrder = Depends(), season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_lineup_spot_for_season_for_all_teams(
        bat_order.number, season.year
    )
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/position/all_teams", response_model=Dict[str, BatStatsSchema])
def get_bat_stats_for_defpos_for_season_for_all_teams(
    def_position: DefensePosition, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_defpos_for_season_for_all_teams(def_position, season.year)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/starters/all_teams", response_model=Dict[str, BatStatsSchema])
def get_bat_stats_for_starters_for_season_for_all_teams(
    season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_starters_for_season_for_all_teams(season.year)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}


@router.get("/subs/all_teams", response_model=Dict[str, BatStatsSchema])
def get_bat_stats_for_subs_for_season_for_all_teams(
    season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    bat_stats_dict = app.scraped_data.get_bat_stats_for_subs_for_season_for_all_teams(season.year)
    if not bat_stats_dict:
        raise HTTPException(status_code=404, detail="No results found")
    return {year: asdict(bat_stats) for year, bat_stats in bat_stats_dict.items()}
