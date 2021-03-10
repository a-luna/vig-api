from fastapi import APIRouter, Depends
from vigorish.app import Vigorish

from app.core.database import get_vig_app
from app.api.api_v1.endpoints.player import bat_stats, pitch_stats

router = APIRouter()


@router.get("/search")
def search_player_name(query: str, app: Vigorish = Depends(get_vig_app)):
    return app.scraped_data.player_name_search(query)


router.include_router(bat_stats.router, prefix="/bat_stats")
router.include_router(pitch_stats.router, prefix="/pitch_stats")
