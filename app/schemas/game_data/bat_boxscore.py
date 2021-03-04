from typing import Dict, Union

from pydantic import BaseModel
from vigorish.enums import DefensePosition


class BatResults(BaseModel):
    team_id: str
    name: str
    mlb_id: int
    bbref_id: str
    is_starter: bool
    bat_order: int
    def_position: DefensePosition
    at_bats: str
    bat_stats: str
    stats_to_date: str


BatBoxscoreSchema = Dict[Union[int, str], BatResults]
