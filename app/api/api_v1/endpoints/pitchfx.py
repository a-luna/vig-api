from typing import List

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish

from app.core import crud
from app.core.database import get_vig_app
from app.schemas import PitchFxSchema


router = APIRouter()


@router.get("/pitch_app", response_model=List[PitchFxSchema])
def get_all_pfx_data_for_pitch_app(game_id: str, pitcher_id: int, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    result = game_data.get_pfx_for_pitcher(pitcher_id)
    if result.failure:
        raise HTTPException(status_code=404, detail="No results found")
    pfx = result.value
    return pfx
