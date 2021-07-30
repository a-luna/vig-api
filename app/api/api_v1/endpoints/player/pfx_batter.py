from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache, cache_one_day, cache_one_week
from vigorish.app import Vigorish
from vigorish.database import PitchFx

from app.api.dependencies import get_date_range, MLBSeason
from app.core.database import get_vig_app
from app.schemas import PitchFxMetricsSchema, PitchFxSchema

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
    all_pfx = app.db_session.query(PitchFx).filter_by(batter_id_mlb=mlb_id).all()
    return [pfx for pfx in all_pfx if pfx.game_date >= start_date and pfx.game_date <= end_date]


@router.get("/", response_model=PitchFxMetricsSchema)
@cache_one_week()
def get_pfx_metrics_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_career_for_batter(mlb_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_rhp_as_rhb", response_model=PitchFxMetricsSchema)
@cache_one_week()
def get_pfx_metrics_vs_rhp_as_rhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_rhp_as_rhb_for_career_for_batter(mlb_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_rhp_as_lhb", response_model=PitchFxMetricsSchema)
@cache_one_week()
def get_pfx_metrics_vs_rhp_as_lhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_rhp_as_lhb_for_career_for_batter(mlb_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_lhp_as_lhb", response_model=PitchFxMetricsSchema)
@cache_one_week()
def get_pfx_metrics_vs_lhp_as_lhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_lhp_as_lhb_for_career_for_batter(mlb_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_lhp_as_rhb", response_model=PitchFxMetricsSchema)
@cache_one_week()
def get_pfx_metrics_vs_lhp_as_rhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_lhp_as_rhb_for_career_for_batter(mlb_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_year", response_model=PitchFxMetricsSchema)
@cache_one_day()
def get_pfx_metrics_for_year_for_batter(
    request: Request,
    response: Response,
    mlb_id: str,
    season: MLBSeason = Depends(),
    app: Vigorish = Depends(get_vig_app),
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_year_for_batter(mlb_id, season.year)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game", response_model=PitchFxMetricsSchema)
@cache()
def get_pfx_metrics_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_for_game_for_batter(mlb_id, game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_rhp_as_rhb", response_model=PitchFxMetricsSchema)
@cache()
def get_pfx_metrics_vs_rhp_as_rhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_rhp_as_rhb_for_game_for_batter(mlb_id, game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_rhp_as_lhb", response_model=PitchFxMetricsSchema)
@cache()
def get_pfx_metrics_vs_rhp_as_lhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_rhp_as_lhb_for_game_for_batter(mlb_id, game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_lhp_as_lhb", response_model=PitchFxMetricsSchema)
@cache()
def get_pfx_metrics_vs_lhp_as_lhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_lhp_as_lhb_for_game_for_batter(mlb_id, game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_lhp_as_rhb", response_model=PitchFxMetricsSchema)
@cache()
def get_pfx_metrics_vs_lhp_as_rhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    pfx_stats = app.scraped_data.get_pfx_metrics_vs_lhp_as_rhb_for_game_for_batter(mlb_id, game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()
