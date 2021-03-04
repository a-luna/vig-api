from fastapi import APIRouter

from app.api.api_v1.endpoints.team_data import pitch_stats


router = APIRouter()
router.include_router(pitch_stats.router, prefix="/pitch_stats")
