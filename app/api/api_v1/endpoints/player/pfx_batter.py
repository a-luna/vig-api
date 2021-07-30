from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_redis_cache import cache, cache_one_day, cache_one_week
from vigorish.app import Vigorish
from vigorish.database import PitchFx

from app.api.dependencies import get_date_range, MLBSeason
from app.core import crud
from app.core.database import get_vig_app
from app.schemas import PitchFxMetricsSetSchema, PitchFxSchema

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
    return (
        app.db_session.query(PitchFx)
        .filter(PitchFx.batter_id == player_data.player.id)
        .filter(PitchFx.game_date >= start_date)
        .filter(PitchFx.game_date <= end_date)
        .all()
    )


@router.get("/", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_all_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_rhp", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_rhp_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_rhp_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_lhp", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_lhp_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_lhp_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_rhp_as_rhb", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_rhp_as_rhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_rhp_as_rhb_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_rhp_as_lhb", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_rhp_as_lhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_rhp_as_lhb_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_lhp_as_lhb", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_lhp_as_lhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_lhp_as_lhb_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/vs_lhp_as_rhb", response_model=PitchFxMetricsSetSchema)
@cache_one_week()
def get_pfx_metrics_vs_lhp_as_rhb_for_career_for_batter(
    request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.pfx_batting_metrics_vs_lhp_as_rhb_for_career
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_year", response_model=PitchFxMetricsSetSchema)
@cache_one_day()
def get_pfx_metrics_for_year_for_batter(
    request: Request,
    response: Response,
    mlb_id: str,
    season: MLBSeason = Depends(),
    app: Vigorish = Depends(get_vig_app),
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_pitching_metrics_vs_all_for_season(season.year)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_all_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_rhp", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_rhp_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_rhp_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_lhp", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_lhp_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_lhp_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_rhp_as_rhb", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_rhp_as_rhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_rhp_as_rhb_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_rhp_as_lhb", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_rhp_as_lhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_rhp_as_lhb_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_lhp_as_lhb", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_lhp_as_lhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_lhp_as_lhb_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()


@router.get("/for_game/vs_lhp_as_rhb", response_model=PitchFxMetricsSetSchema)
@cache()
def get_pfx_metrics_vs_lhp_as_rhb_for_game_for_batter(
    request: Request, response: Response, mlb_id: str, game_id: str, app: Vigorish = Depends(get_vig_app)
):
    player_data = crud.get_player_data(mlb_id, app)
    pfx_stats = player_data.get_pfx_batting_metrics_vs_lhp_as_rhb_for_game(game_id)
    if not pfx_stats:
        raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
    return pfx_stats.as_dict()
