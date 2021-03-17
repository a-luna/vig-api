from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.util.string_helpers import validate_at_bat_id


from app.core import crud
from app.core.database import get_vig_app
from app.schemas import AtBatSchema, BatBoxscoreSchema, PitchBoxscoreSchema, TeamDataSchema


router = APIRouter()


@router.get("/away", response_model=TeamDataSchema)
def get_away_team_data(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.team_data[game_data.away_team_id]


@router.get("/home", response_model=TeamDataSchema)
def get_home_team_data(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.team_data[game_data.home_team_id]


@router.get("/away/batting", response_model=BatBoxscoreSchema)
def get_away_team_bat_boxscore(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.bat_boxscore[game_data.away_team_id]


@router.get("/home/batting", response_model=BatBoxscoreSchema)
def get_home_team_bat_boxscore(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.bat_boxscore[game_data.home_team_id]


@router.get("/away/pitching", response_model=PitchBoxscoreSchema)
def get_away_team_pitch_boxscore(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.pitch_boxscore[game_data.away_team_id]


@router.get("/home/pitching", response_model=PitchBoxscoreSchema)
def get_home_team_pitch_boxscore(game_id: str, app: Vigorish = Depends(get_vig_app)):
    game_data = crud.get_game_data(game_id, app)
    return game_data.pitch_boxscore[game_data.home_team_id]


@router.get("/pbp", response_model=AtBatSchema)
def get_play_by_play_for_at_bat(at_bat_id: str, app: Vigorish = Depends(get_vig_app)):
    result = validate_at_bat_id(at_bat_id)
    if result.failure:
        raise HTTPException(status_code=404, detail=f"At Bat ID: {at_bat_id} is invalid")
    game_id = result.value["game_id"]
    game_data = crud.get_game_data(game_id, app)
    at_bat_data = game_data.at_bat_map.get(at_bat_id)
    if not at_bat_data:
        raise HTTPException(status_code=404, detail="No results found")
    return at_bat_data
