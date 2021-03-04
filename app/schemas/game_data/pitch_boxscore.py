from typing import Dict, Union

from pydantic import BaseModel


class PitchResults(BaseModel):
    team_id: str
    name: str
    mlb_id: int
    bbref_id: str
    pitch_app_type: str
    game_results: str


PitchBoxscoreSchema = Dict[Union[int, str], PitchResults]
