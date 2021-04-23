from http import HTTPStatus
from typing import List, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish
from vigorish.util.string_helpers import validate_at_bat_id

from app.api.dependencies import get_pitch_app_params
from app.core import crud
from app.core.database import get_vig_app
from app.schemas import PitchFxSchema

router = APIRouter()


@router.get("/pitch_app", response_model=List[PitchFxSchema])
@cache()
def get_all_pfx_data_for_pitch_app(
    request: Request,
    response: Response,
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    game_data = crud.get_game_data(game_id, app)
    result = game_data.get_pfx_for_pitcher(mlb_id)
    if result.failure:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    pfx = result.value
    if not pfx:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return pfx


@router.get("/at_bat", response_model=List[PitchFxSchema])
@cache()
def get_all_pfx_data_for_at_bat(
    request: Request, response: Response, at_bat_id: str, app: Vigorish = Depends(get_vig_app)
):
    result = validate_at_bat_id(at_bat_id)
    if result.failure:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    at_bat_dict = result.value
    game_data = crud.get_game_data(at_bat_dict["game_id"], app)
    pfx = game_data.get_pfx_for_at_bat(at_bat_id)
    if not pfx:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return pfx
