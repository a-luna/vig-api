from typing import Dict, Union

from vigorish.models.player import Player

from app.schemas import PlayerSchema


def convert_player_to_dict(player: Player) -> Dict[str, Union[str, int]]:
    return PlayerSchema.from_orm(player).dict()
