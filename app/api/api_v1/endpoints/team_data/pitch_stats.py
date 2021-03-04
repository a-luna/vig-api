from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import PitchStatsSchema


router = APIRouter()


@router.get("/sp_by_player", response_model=List[PitchStatsSchema])
def get_pitch_stats_for_sp_by_player_for_team(team_id: str, year: int, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_for_sp_by_player_for_team(team_id, year)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]
