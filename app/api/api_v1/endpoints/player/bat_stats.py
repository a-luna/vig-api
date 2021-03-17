from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import BatStatsSchema


router = APIRouter()


@router.get("/", response_model=BatStatsSchema)
def get_bat_stats_for_career_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_for_career_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(bat_stats)


@router.get("/by_year", response_model=List[BatStatsSchema])
def get_bat_stats_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/by_team", response_model=List[BatStatsSchema])
def get_bat_stats_by_team_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_team_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/by_team_by_year", response_model=List[BatStatsSchema])
def get_bat_stats_by_team_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_team_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/by_opp_team", response_model=List[BatStatsSchema])
def get_bat_stats_by_opp_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]


@router.get("/by_opp_team_by_year", response_model=List[BatStatsSchema])
def get_bat_stats_by_opp_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    bat_stats = app.scraped_data.get_bat_stats_by_opp_by_year_for_player(mlb_id)
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]
