from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PlayerDefPosMetricsSchema(BaseModel):
    def_pos: str
    percent: int


class PlayerBatOrderMetricsSchema(BaseModel):
    bat_order: int
    percent: int


class PlayerTeamSchema(BaseModel):
    mlb_id: int
    bbref_id: str
    team_id: str
    year: int
    role: str
    stint_number: int
    starting_lineup: bool
    percent_started: int
    bench_player: bool
    percent_bench: int
    starting_pitcher: bool
    percent_sp: int
    relief_pitcher: bool
    percent_rp: int
    def_pos_list: List[PlayerDefPosMetricsSchema]
    bat_order_list: List[PlayerBatOrderMetricsSchema]


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
    all_teams: List[PlayerTeamSchema]


class FuzzySearchResult(BaseModel):
    match: str
    score: int
    result: int
    details: Optional[PlayerDetailsSchema]
