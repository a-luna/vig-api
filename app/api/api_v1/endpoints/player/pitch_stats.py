from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.schemas import PitchStatsSchema


router = APIRouter()


@router.get("/", response_model=PitchStatsSchema)
def get_pitch_stats_for_career_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_for_career_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/as_sp", response_model=PitchStatsSchema)
def get_pitch_stats_as_sp_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_as_sp_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/as_rp", response_model=PitchStatsSchema)
def get_pitch_stats_as_rp_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_as_rp_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return asdict(pitch_stats)


@router.get("/by_year", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/by_team", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_team_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_team_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/by_team_by_year", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_team_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_team_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/by_opp_team", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_opp_team_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_opp_team_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]


@router.get("/by_opp_team_by_year", response_model=List[PitchStatsSchema])
def get_pitch_stats_by_opp_team_by_year_for_player(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pitch_stats = app.scraped_data.get_pitch_stats_by_opp_team_by_year_for_player(mlb_id)
    if not pitch_stats:
        raise HTTPException(status_code=404, detail="No results found")
    return [asdict(s) for s in pitch_stats]
