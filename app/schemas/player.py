from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PlayerTeamSchema(BaseModel):
    team_id: Optional[str]
    year: Optional[int]
    pos: Optional[str]


class PlayerDetailsSchema(BaseModel):
    name_first: str
    name_last: str
    name_given: str
    bats: str
    throws: str
    weight: int
    height: int
    debut: datetime
    birth_year: int
    birth_month: int
    birth_day: int
    birth_country: Optional[str]
    birth_state: Optional[str]
    birth_city: Optional[str]
    bbref_id: str
    mlb_id: int
    current_team: PlayerTeamSchema
    previous_teams: List[str]


class FuzzySearchResult(BaseModel):
    match: str
    score: int
    result: int
    details: Optional[PlayerDetailsSchema]
