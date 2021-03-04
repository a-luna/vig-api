from typing import Dict, List, Optional

from pydantic import BaseModel


class BatStatDetailSchema(BaseModel):
    count: int
    stat: str


class LineupSpotSchema(BaseModel):
    player_id_br: str
    bat_order: int
    def_position: str


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
    batter_name: str
    batter_id_mlb: int
    batter_id_bbref: str
    batter_team_id_bb: str
    batter_team_id_bbref: str
    opponent_team_id_bb: str
    opponent_team_id_bbref: str
    total_pbp_events: int
    total_incomplete_at_bats: int
    total_plate_appearances: int
    at_bat_ids: List[str]
    incomplete_at_bat_ids: List[str]
    bbref_data: BBRefBatDataSchema


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


class PitchStatsSchema(BaseModel):
    pitcher_name: str
    pitcher_id_mlb: int
    pitcher_id_bbref: str
    pitch_app_id: str
    pitcher_team_id_bb: str
    pitcher_team_id_bbref: str
    opponent_team_id_bb: str
    opponent_team_id_bbref: str
    bb_game_id: str
    bbref_game_id: str
    pitch_count_by_inning: Dict[str, int]
    pitch_count_by_pitch_type: Dict[str, int]
    bbref_data: BBRefPitchDataSchema


class TeamDataSchema(BaseModel):
    team_id_br: str
    total_wins_before_game: int
    total_losses_before_game: int
    total_runs_scored_by_team: int
    total_runs_scored_by_opponent: int
    total_hits_by_team: int
    total_hits_by_opponent: int
    total_errors_by_team: int
    total_errors_by_opponent: int
    team_won: bool
    pitcher_of_record: str
    pitcher_earned_save: str
    starting_lineup: List[LineupSpotSchema]
    batting_stats: List[BatStatsSchema]
    pitching_stats: List[PitchStatsSchema]
