from typing import Optional
from pydantic import BaseModel


class GamePitchStatsSchema(BaseModel):
    bbref_game_id: str
    player_id_mlb: int
    player_id_bbref: str
    player_team_id_bbref: str
    opponent_team_id_bbref: str
    is_sp: int
    is_rp: int
    is_wp: int
    is_lp: int
    is_sv: int
    innings_pitched: float
    total_outs: int
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
    player_name: Optional[str] = ""
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    saves: Optional[int] = 0
    full_stat_line: Optional[str] = ""
    summary_stat_line: Optional[str] = ""
    csw: Optional[int] = 0

    class Config:
        orm_mode = True


class CombinedPitchStatsSchema(BaseModel):
    year: int
    team_id_bbref: str
    opponent_team_id_bbref: str
    player_name: str
    mlb_id: int
    bbref_id: str
    stint_number: int
    total_games: int
    games_as_sp: int
    games_as_rp: int
    wins: int
    losses: int
    saves: int
    innings_pitched: float
    total_outs: int
    batters_faced: int
    runs: int
    earned_runs: int
    hits: int
    homeruns: int
    strikeouts: int
    bases_on_balls: int
    era: float
    whip: float
    k_per_nine: float
    bb_per_nine: float
    hr_per_nine: float
    k_per_bb: float
    k_rate: float
    bb_rate: float
    k_minus_bb: float
    hr_per_fb: float
    pitch_count: int
    strikes: int
    strikes_contact: int
    strikes_swinging: int
    strikes_looking: int
    ground_balls: int
    fly_balls: int
    line_drives: int
    unknown_type: int
    inherited_runners: int
    inherited_scored: int
    wpa_pitch: float
    re24_pitch: float
    league: Optional[str]
    division: Optional[str]
