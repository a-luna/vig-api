from fastapi import APIRouter

from app.api.api_v1.endpoints.player_data import bat_stats


router = APIRouter()
router.include_router(bat_stats.router, prefix="/bat_stats")
