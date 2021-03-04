from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish

from app.core import crud
from app.core.database import get_vig_app
from app.schemas import BatStatsSchema


router = APIRouter()


@router.get("/by_team_by_year", response_model=List[BatStatsSchema])
def get_bat_stats_by_team_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    bat_stats = player_data.bat_stats_by_team_by_year
    if not bat_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in bat_stats]
