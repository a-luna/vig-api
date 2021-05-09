from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish
from vigorish.util.string_helpers import validate_at_bat_id

from app.core import crud
from app.core.database import get_vig_app
from app.schema_prep import convert_boxscore_data
from app.schemas import AtBatSchema, BoxscoreSchema

router = APIRouter()


@router.get("/boxscore", response_model=BoxscoreSchema, response_model_exclude_unset=True)
@cache()
def get_boxscore_for_game(request: Request, response: Response, game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return convert_boxscore_data(game_data.get_boxscore_data())


@router.get("/all_pbp", response_model=List[AtBatSchema])
@cache()
def get_play_by_play_for_game(request: Request, response: Response, game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.get_all_at_bats_no_pfx()


@router.get("/pbp", response_model=AtBatSchema)
@cache()
def get_play_by_play_for_at_bat(
    request: Request, response: Response, at_bat_id: str, app: Vigorish = Depends(get_vig_app)
):
    result = validate_at_bat_id(at_bat_id)
    if result.failure:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=f"At Bat ID: {at_bat_id} is invalid")
    game_id = result.value["game_id"]
    game_data = crud.get_game_data(game_id, app)
    at_bat_data = game_data.get_pbp_for_at_bat(at_bat_id)
    if not at_bat_data:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return at_bat_data
