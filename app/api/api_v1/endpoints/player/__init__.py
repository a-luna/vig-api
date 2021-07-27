from typing import List

from fastapi import APIRouter, Depends, Request, Response
from fastapi_redis_cache import cache
from vigorish.app import Vigorish

from app.api.api_v1.endpoints.player import bat_stats, pfx_batter, pfx_pitcher, pitch_stats
from app.core import crud
from app.core.database import get_vig_app
from app.schemas import FuzzySearchResult, PlayerDetailsSchema

router = APIRouter()


@router.get("/search", response_model=List[FuzzySearchResult], tags=["player search"])
def search_player_name(query: str, app: Vigorish = Depends(get_vig_app)):
    results = app.scraped_data.player_name_search(query)
    for player_match in results:
        player_data = crud.get_player_data(player_match["result"], app)
        if player_data:
            player_match["details"] = player_data.player_details
    return results


@router.get("/details", response_model=PlayerDetailsSchema, tags=["player search"])
@cache()
def get_player_details(request: Request, response: Response, mlb_id: str, app: Vigorish = Depends(get_vig_app)):
    player_data = crud.get_player_data(mlb_id, app)
    return player_data.player_details


router.include_router(bat_stats.router, prefix="/batting", tags=["player batting"])
router.include_router(pitch_stats.router, prefix="/pitching", tags=["player pitching"])
router.include_router(pfx_batter.router, prefix="/batting/pfx", tags=["player pfx batting"])
router.include_router(pfx_pitcher.router, prefix="/pitching/pfx", tags=["player pfx pitching"])
