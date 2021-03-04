from fastapi import APIRouter

from app.api.api_v1.endpoints import game_data, pitchfx, player_data, team_data


api_router = APIRouter()
api_router.include_router(game_data.router, prefix="/game", tags=["game_data"])
api_router.include_router(pitchfx.router, prefix="/pfx", tags=["pitchfx"])
api_router.include_router(player_data.router, prefix="/player", tags=["player_data"])
api_router.include_router(team_data.router, prefix="/team", tags=["team_data"])
