from typing import List
from fastapi import APIRouter, Depends
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.api.api_v1.endpoints.player import bat_stats, pitch_stats, pfx_batter, pfx_pitcher
from app.schemas import FuzzySearchResult

router = APIRouter()


@router.get("/search", response_model=List[FuzzySearchResult])
def search_player_name(query: str, app: Vigorish = Depends(get_vig_app)):
    return app.scraped_data.player_name_search(query)


router.include_router(bat_stats.router, prefix="/batting", tags=["player batting"])
router.include_router(pitch_stats.router, prefix="/pitching", tags=["player pitching"])
router.include_router(pfx_batter.router, prefix="/batting/pfx", tags=["player pfx batting"])
router.include_router(pfx_pitcher.router, prefix="/pitching/pfx", tags=["player pfx pitching"])
