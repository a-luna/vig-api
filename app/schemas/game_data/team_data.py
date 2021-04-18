from typing import Dict, List, Optional

from pydantic import BaseModel
from vigorish.enums import DefensePosition

from app.schemas.game_data.at_bat import PlayerSubEvent


class BatStatDetailSchema(BaseModel):
    count: int
    stat: str


class BBRefBatDataSchema(BaseModel):
    plate_appearances: int
    at_bats: int
    hits: int
    runs_scored: int
    rbis: int
    bases_on_balls: int
    strikeouts: int
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
    details: Optional[List[BatStatDetailSchema]]


class BatStatsSchema(BaseModel):
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
    total_pbp_events: int
    total_incomplete_at_bats: int
    total_plate_appearances: int
    at_bat_ids: List[str]
    incomplete_at_bat_ids: List[str]
    substitutions: Optional[List[PlayerSubEvent]]
    bbref_data: BBRefBatDataSchema


class AtBatSummarySchema(BaseModel):
    pbp_table_row_number: int
    batter_name: str
    pitcher_name: str
    inning: str
    runners_on_base: str
    outs: int
    play_description: str
    pitch_sequence: str


class BBRefPitchDataSchema(BaseModel):
    innings_pitched: float
    hits: int
    runs: int
    earned_runs: int
    bases_on_balls: int
    strikeouts: int
    homeruns: int
    batters_faced: int
    pitch_count: int
    strikes: int
    strikes_contact: int
    strikes_swinging: int
    strikes_looking: int
    ground_balls: int
    fly_balls: int
    line_drives: int
    unknown_type: int
    game_score: int
    inherited_runners: int
    inherited_scored: int
    wpa_pitch: float
    avg_lvg_index: float
    re24_pitch: float


class InningTotalsSchema(BaseModel):
    outs: int
    hits: int
    runs: int
    bb: int
    so: int
    bf: int
    pitch_count: int
    strikes: int


class PitchStatsSchema(BaseModel):
    team_id: str
    name: str
    mlb_id: int
    bbref_id: str
    pitch_app_type: str
    game_results: str
    pitch_app_id: str
    pitch_count_by_inning: Dict[str, int]
    pitch_count_by_pitch_type: Dict[str, int]
    at_bat_ids: List[str]
    substitutions: Optional[List[PlayerSubEvent]]
    bbref_data: BBRefPitchDataSchema


class HtmlBatStatsSchema(BaseModel):
    row_id: int
    name: str
    mlb_id: int
    is_starter: bool
    bat_order: int
    def_position: int
    position_start: str
    position_changes: str
    stat_line: str
    plate_appearances: int
    at_bats: int
    hits: int
    runs_scored: int
    rbis: int
    bases_on_balls: int
    strikeouts: int
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
    details: Optional[List[BatStatDetailSchema]]
    at_bat_results: List[AtBatSummarySchema]
    incomplete_at_bat_ids: List[str]
    substitutions: Optional[List[PlayerSubEvent]]


class HtmlPitchStatsSchema(BaseModel):
    row_id: int
    name: str
    mlb_id: int
    pitch_app_type: str
    stat_line: str
    pitch_app_id: str
    innings_pitched: float
    hits: int
    runs: int
    earned_runs: int
    bases_on_balls: int
    strikeouts: int
    homeruns: int
    batters_faced: int
    pitch_count: int
    strikes: int
    strikes_contact: int
    strikes_swinging: int
    strikes_looking: int
    ground_balls: int
    fly_balls: int
    line_drives: int
    unknown_type: int
    game_score: int
    inherited_runners: int
    inherited_scored: int
    wpa_pitch: float
    avg_lvg_index: float
    re24_pitch: float
    at_bat_ids: List[str]
    inning_totals: Dict[int, InningTotalsSchema]
    substitutions: Optional[List[PlayerSubEvent]]


class TeamDataSchema(BaseModel):
    team_id: str
    team_name: str
    total_wins: int
    total_losses: int
    runs_scored_by_team: int
    runs_scored_by_opponent: int
    team_won: bool
    pitcher_of_record: str
    pitcher_earned_save: str
    batting: List[HtmlBatStatsSchema]
    pitching: List[HtmlPitchStatsSchema]
