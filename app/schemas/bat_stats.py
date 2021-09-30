from typing import List, Optional
from pydantic import BaseModel
from vigorish.enums import DefensePosition


class GameBatStatsSchema(BaseModel):
    bbref_game_id: str
    player_id_mlb: int
    player_id_bbref: str
    player_team_id_bbref: str
    opponent_team_id_bbref: str
    is_starter: int
    bat_order: int
    def_position: str
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
    avg_to_date: float
    obp_to_date: float
    slg_to_date: float
    ops_to_date: float
    total_pitches: int
    total_strikes: int
    wpa_bat: float
    avg_lvg_index: float
    wpa_bat_pos: float
    wpa_bat_neg: float
    re24_bat: float
    extra_base_hits: Optional[int] = 0
    total_bases: Optional[int] = 0
    player_name: Optional[str] = ""
    stat_line: Optional[str] = ""

    class Config:
        orm_mode = True


class DefPosMetricsSchema(BaseModel):
    def_pos: DefensePosition
    is_starter: bool
    total_games: int
    percent: float


class BatOrderMetricsSchema(BaseModel):
    bat_order: int
    total_games: int
    percent: float


class CombinedBatStatsSchema(BaseModel):
    year: Optional[int]
    player_team_id_bbref: Optional[str]
    opponent_team_id_bbref: Optional[str]
    player_name: Optional[str]
    is_starter: bool
    bat_order: Optional[str]
    bat_order_list: Optional[List[int]]
    bat_order_metrics: Optional[List[BatOrderMetricsSchema]]
    def_position: Optional[str]
    def_position_list: Optional[List[DefensePosition]]
    def_position_metrics: Optional[List[DefPosMetricsSchema]]
    mlb_id: Optional[int]
    bbref_id: Optional[str]
    stint_number: Optional[int]
    total_games: int
    total_games_started: int
    total_games_subbed: int
    percent_started: float
    percent_subbed: float
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
    age: Optional[int]
    league: Optional[str]
    division: Optional[str]
    changed_teams_midseason: Optional[bool] = False
    all_stats_for_season: Optional[bool] = False
    all_stats_for_stint: Optional[bool] = False
    career_stats_all_teams: Optional[bool] = False
    career_stats_for_team: Optional[bool] = False
    all_team_stats_for_def_pos: Optional[bool] = False
    all_player_stats_for_def_pos: Optional[bool] = False
    separate_player_stats_for_def_pos: Optional[bool] = False
    all_team_stats_for_bat_order: Optional[bool] = False
    all_player_stats_for_bat_order: Optional[bool] = False
    separate_player_stats_for_bat_order: Optional[bool] = False
    total_seasons: Optional[int]
    row_id: Optional[str]


class CareerBatStatsSchema(BaseModel):
    career: CombinedBatStatsSchema
    by_team: List[CombinedBatStatsSchema]
    by_team_by_year: List[CombinedBatStatsSchema]
