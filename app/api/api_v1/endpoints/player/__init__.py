from typing import List

from fastapi import APIRouter, Depends, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish

from app.api.api_v1.endpoints.player import bat_stats, pfx_batter, pfx_pitcher, pitch_stats
from app.core.crud import get_player
from app.core.database import get_vig_app
from app.schemas import FuzzySearchResult, PlayerSchema

router = APIRouter()


@router.get("/search", response_model=List[FuzzySearchResult], tags=["player search"])
def search_player_name(query: str, app: Vigorish = Depends(get_vig_app)):
    return app.scraped_data.player_name_search(query)


@router.get("/details", response_model=PlayerSchema, tags=["player search"])
@cache()
def get_player_details(request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    return get_player(mlb_id, app)


router.include_router(bat_stats.router, prefix="/batting", tags=["player batting"])
router.include_router(pitch_stats.router, prefix="/pitching", tags=["player pitching"])
router.include_router(pfx_batter.router, prefix="/batting/pfx", tags=["player pfx batting"])
router.include_router(pfx_pitcher.router, prefix="/pitching/pfx", tags=["player pfx pitching"])
