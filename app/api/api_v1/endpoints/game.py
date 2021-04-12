from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.util.string_helpers import validate_at_bat_id

from app.core import crud
from app.core.cache import cache
from app.core.database import get_vig_app
from app.schema_prep import convert_boxscore_data
from app.schemas import AtBatSchema, BoxscoreSchema

router = APIRouter()


@router.get("/boxscore", response_model=BoxscoreSchema, response_model_exclude_unset=True)
@cache()
def get_boxscore_for_game(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return convert_boxscore_data(game_data.get_boxscore_data())


@router.get("/pbp", response_model=AtBatSchema)
@cache()
def get_play_by_play_for_at_bat(at_bat_id: str, app: Vigorish = Depends(get_vig_app)):
    result = validate_at_bat_id(at_bat_id)
    if result.failure:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"At Bat ID: {at_bat_id} is invalid")
    game_id = result.value["game_id"]
    game_data = crud.get_game_data(game_id, app)
    at_bat_data = game_data.at_bat_map.get(at_bat_id)
    if not at_bat_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return at_bat_data
