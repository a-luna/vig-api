from fastapi import APIRouter

from app.api.api_v1.endpoints.team import bat_stats, pitch_stats


router = APIRouter()
router.include_router(bat_stats.router, prefix="/batting", tags=["team batting"])
router.include_router(pitch_stats.router, prefix="/pitching", tags=["team pitching"])
