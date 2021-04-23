from pydantic import BaseModel
from vigorish.enums import DefensePosition


class BatStatsSchema(BaseModel):
    year: int
    team_id_bbref: str
    opponent_team_id_bbref: str
    is_starter: bool
    bat_order: int
    def_position: DefensePosition
    mlb_id: int
    bbref_id: str
    stint_number: int
    total_games: int
    avg: float
    obp: float
    slg: float
    ops: float
    iso: float
    bb_rate: float
    k_rate: float
    contact_rate: float
    plate_appearances: int
    at_bats: int
    hits: int
    runs_scored: int
    rbis: int
    bases_on_balls: int
    strikeouts: int
    doubles: int
    triples: int
    homeruns: int
    stolen_bases: int
    caught_stealing: int
    hit_by_pitch: int
    intentional_bb: int
    gdp: int
    sac_fly: int
    sac_hit: int
    total_pitches: int
    total_strikes: int
    wpa_bat: float
    wpa_bat_pos: float
    wpa_bat_neg: float
    re24_bat: float
