import json
from http import HTTPStatus
from pathlib import Path
from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache_one_day
from vigorish.app import Vigorish
from vigorish.util.list_helpers import flatten_list2d

from app.api.dependencies import get_date_range, get_pitch_app_params, MLBSeason
from app.core import crud
from app.core.config import settings
from app.core.database import get_vig_app
from app.schema_prep import combine_career_and_yearly_pfx_metrics_sets
from app.schemas import (
    CareerPfxMetricsForPitcherSchema,
    PitchTypePercentilesSchema,
    PitchFxMetricsSetSchema,
    PitchFxSchema,
)

router = APIRouter()


@router.get("/in_date_range", response_model=List[PitchFxSchema])
def get_all_pfx_within_date_range_for_player(
    request: Request,
    response: Response,
    mlb_id: int,
    date_range: tuple = Depends(get_date_range),
    app: Vigorish = Depends(get_vig_app),
):
    start_date, end_date = date_range
    player_data = crud.get_player_data(mlb_id, app)
    all_pfx = [
        p.pitchfx for p in player_data.pitch_app_map.values() if p.game_date >= start_date and p.game_date <= end_date
    ]
    return flatten_list2d(all_pfx)


@router.get("/", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_career_pfx_metrics_for_pitcher(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_pitching_metrics_vs_all_by_year
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/percentiles", response_model=List[PitchTypePercentilesSchema])
@cache_one_day()
def get_career_percentiles_for_pitch_types(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_for_career


@router.get("/vs_RHB", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_career_pfx_metrics_vs_rhb_for_pitcher(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_pitching_metrics_vs_rhb_for_career
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_RHB/percentiles", response_model=List[PitchTypePercentilesSchema])
@cache_one_day()
def get_career_percentiles_vs_rhb_for_pitch_types(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_rhb_for_career


@router.get("/vs_LHB", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_career_pfx_metrics_vs_lhb_for_pitcher(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_pitching_metrics_vs_lhb_for_career
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_LHB/percentiles", response_model=List[PitchTypePercentilesSchema])
@cache_one_day()
def get_career_percentiles_vs_lhb_for_pitch_types(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_lhb_for_career


@router.get("/career_pfx", response_model=CareerPfxMetricsForPitcherSchema)
@cache_one_day()
def get_all_pfx_career_data(request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    if settings.ENV == "DEV":
        mock_data_file = Path(__file__).parent.joinpath("combined_pfx.json")
        return json.loads(mock_data_file.read_text())
    player_data = crud.get_player_data(mlb_id, app)
    career_pfx = player_data.get_all_pfx_career_data()
    yearly_pfx = player_data.get_all_pfx_yearly_data()
    return combine_career_and_yearly_pfx_metrics_sets(career_pfx, yearly_pfx)


@router.get("/for_year", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_for_year_for_pitcher(
    request: Request,
    response: Response,
    mlb_id: str,
    season: MLBSeason = Depends(),
    app: Vigorish = Depends(get_vig_app),
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_pitching_metrics_vs_all_for_season(season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/by_year/percentiles", response_model=Dict[int, List[PitchTypePercentilesSchema]])
@cache_one_day()
def get_percentiles_for_pitch_types_by_year(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_by_year


@router.get("/vs_RHB/for_year", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_vs_rhb_for_year_for_pitcher(
    request: Request,
    response: Response,
    mlb_id: str,
    season: MLBSeason = Depends(),
    app: Vigorish = Depends(get_vig_app),
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_pitching_metrics_vs_rhb_for_season(season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_RHB/by_year/percentiles", response_model=Dict[int, List[PitchTypePercentilesSchema]])
@cache_one_day()
def get_percentiles_vs_rhb_for_pitch_types_by_year(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_rhb_by_year


@router.get("/vs_LHB/for_year", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_vs_lhb_for_year_for_pitcher(
    request: Request,
    response: Response,
    mlb_id: str,
    season: MLBSeason = Depends(),
    app: Vigorish = Depends(get_vig_app),
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_pitching_metrics_vs_lhb_for_season(season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_LHB/by_year/percentiles", response_model=Dict[int, List[PitchTypePercentilesSchema]])
@cache_one_day()
def get_percentiles_vs_lhb_for_pitch_types_by_year(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_lhb_by_year


@router.get("/for_game", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_for_game_for_pitcher(
    request: Request,
    response: Response,
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_pitching_metrics_vs_all_for_game(game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_RHB", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_for_game_vs_rhb_for_pitcher(
    request: Request,
    response: Response,
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_vs_rhb_for_pitcher(mlb_id, game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_LHB", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_for_game_vs_lhb_for_pitcher(
    request: Request,
    response: Response,
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_vs_lhb_for_pitcher(mlb_id, game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()
