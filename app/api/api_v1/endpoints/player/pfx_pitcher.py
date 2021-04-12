from http import HTTPStatus
from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.util.list_helpers import flatten_list2d

from app.core import crud
from app.core.cache import cache
from app.api.dependencies import get_date_range, get_pitch_app_params, MLBSeason
from app.core.database import get_vig_app
from app.schemas import PitchFxSchema, PfxPercentileSchema, PfxPitchingStatsCollectionSchema
from app.schemas.pfx_stats import prepare_pfx_response_model


router = APIRouter()


@router.get("/in_date_range", response_model=List[PitchFxSchema])
@cache()
def get_all_pfx_within_date_range_for_player(
    mlb_id: int, date_range: tuple = Depends(get_date_range), app: Vigorish = Depends(get_vig_app)
):
    start_date, end_date = date_range
    player_data = crud.get_player_data(mlb_id, app)
    all_pfx = [
        p.pitchfx for p in player_data.pitch_app_map.values() if p.game_date >= start_date and p.game_date <= end_date
    ]
    return flatten_list2d(all_pfx)


@router.get("/", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_career_pfx_metrics_for_pitcher(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pfx_stats = app.scraped_data.get_career_pfx_metrics_for_pitcher(mlb_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/percentiles", response_model=List[PfxPercentileSchema])
@cache()
def get_career_percentiles_for_pitch_types(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_for_career


@router.get("/vs_RHB", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_career_pfx_metrics_vs_rhb_for_pitcher(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pfx_stats = app.scraped_data.get_career_pfx_metrics_vs_rhb_for_pitcher(mlb_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/vs_RHB/percentiles", response_model=List[PfxPercentileSchema])
@cache()
def get_career_percentiles_vs_rhb_for_pitch_types(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_rhb_for_career


@router.get("/vs_LHB", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_career_pfx_metrics_vs_lhb_for_pitcher(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    pfx_stats = app.scraped_data.get_career_pfx_metrics_vs_lhb_for_pitcher(mlb_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/vs_LHB/percentiles", response_model=List[PfxPercentileSchema])
@cache()
def get_career_percentiles_vs_lhb_for_pitch_types(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_lhb_for_career


@router.get("/for_year", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_for_year_for_pitcher(
    mlb_id: str, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_year_for_pitcher(mlb_id, season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/by_year/percentiles", response_model=Dict[int, List[PfxPercentileSchema]])
@cache()
def get_percentiles_for_pitch_types_by_year(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_by_year


@router.get("/vs_RHB/for_year", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_vs_rhb_for_year_for_pitcher(
    mlb_id: str, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_year_vs_rhb_for_pitcher(mlb_id, season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/vs_RHB/by_year/percentiles", response_model=Dict[int, List[PfxPercentileSchema]])
@cache()
def get_percentiles_vs_rhb_for_pitch_types_by_year(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_rhb_by_year


@router.get("/vs_LHB/for_year", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_vs_lhb_for_year_for_pitcher(
    mlb_id: str, season: MLBSeason = Depends(), app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_year_vs_lhb_for_pitcher(mlb_id, season.year)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/vs_LHB/by_year/percentiles", response_model=Dict[int, List[PfxPercentileSchema]])
@cache()
def get_percentiles_vs_lhb_for_pitch_types_by_year(mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.percentiles_for_pitch_types_vs_lhb_by_year


@router.get("/for_game", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_for_game_for_pitcher(
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_for_pitcher(mlb_id, game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/for_game/vs_RHB", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_for_game_vs_rhb_for_pitcher(
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_vs_rhb_for_pitcher(mlb_id, game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)


@router.get("/for_game/vs_LHB", response_model=PfxPitchingStatsCollectionSchema)
@cache()
def get_pfx_metrics_for_game_vs_lhb_for_pitcher(
    pitch_app_params: Tuple = Depends(get_pitch_app_params),
    app: Vigorish = Depends(get_vig_app),
):
    mlb_id, game_id = pitch_app_params
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_vs_lhb_for_pitcher(mlb_id, game_id)
    if not pfx_stats or not pfx_stats.total_pitches:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No results found")
    return prepare_pfx_response_model(pfx_stats)
