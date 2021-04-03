from typing import List
from pydantic import BaseModel


class TeamSchema(BaseModel):
    year: int
    league: str
    team_id: str
    franch_id: str
    division: str
    games: int
    games_at_home: int
    wins: int
    losses: int
    runs: int
    at_bats: int
    hits: int
    doubles: int
    triples: int
    homeruns: int
    base_on_balls: int
    strikeouts: int
    stolen_bases: int
    caught_stealing: int
    runs_against: int
    earned_runs: int
    saves: int
    ip_outs: int
    errors: int
    name: str
    park: str
    batting_park_factor: int
    pitching_park_factor: int
    team_id_br: str
    team_id_retro: str

    class Config:
        orm_mode = True


class TeamDivMapSchema(BaseModel):
    w: List[TeamSchema]
    c: List[TeamSchema]
    e: List[TeamSchema]


class TeamLeagueStandings(BaseModel):
    al: TeamDivMapSchema
    nl: TeamDivMapSchema
