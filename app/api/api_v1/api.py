from fastapi import APIRouter

from app.api.api_v1.endpoints import game, pfx, player, season, team


api_router = APIRouter()
api_router.include_router(game.router, prefix="/game", tags=["game"])
api_router.include_router(pfx.router, prefix="/pfx", tags=["pitchfx"])
api_router.include_router(player.router, prefix="/player")
api_router.include_router(season.router, prefix="/season", tags=["season"])
api_router.include_router(team.router, prefix="/team")
