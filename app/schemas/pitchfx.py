from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PitchFxSchema(BaseModel):
    bb_game_id: str
    bbref_game_id: str
    pitch_app_id: str
    inning_id: str
    at_bat_id: str
    pitcher_id_mlb: int
    batter_id_mlb: int
    pitcher_id_bbref: str
    batter_id_bbref: str
    pitcher_team_id_bb: str
    opponent_team_id_bb: str
    p_throws: str
    stand: str
    pitch_id: int
    inning: int
    ab_total: int
    ab_count: int
    ab_id: int
    table_row_number: int
    des: str
    strikes: int
    balls: int
    basic_type: str
    pdes: str
    mlbam_pitch_name: str
    park_sv_id: str
    game_start_time_utc: datetime
    time_pitch_thrown_utc: datetime
    seconds_since_game_start: int
    has_zone_location: int
    batter_did_swing: int
    batter_made_contact: int
    called_strike: int
    swinging_strike: int
    inside_strike_zone: int
    outside_strike_zone: int
    swing_inside_zone: int
    swing_outside_zone: int
    contact_inside_zone: int
    contact_outside_zone: int
    is_batted_ball: int
    is_ground_ball: int
    is_fly_ball: int
    is_line_drive: int
    is_pop_up: int
    is_final_pitch_of_ab: int
    ab_result_out: int
    ab_result_hit: int
    ab_result_single: int
    ab_result_double: int
    ab_result_triple: int
    ab_result_homerun: int
    ab_result_bb: int
    ab_result_ibb: int
    ab_result_k: int
    ab_result_hbp: int
    ab_result_error: int
    ab_result_sac_hit: int
    ab_result_sac_fly: int
    ab_result_unclear: int
    pitch_type_int: int
    pbp_play_result: str
    pbp_runs_outs_result: str
    is_sp: int
    is_rp: int
    is_patched: int
    is_invalid_ibb: int
    is_out_of_sequence: int
    start_speed: Optional[float] = 0.0
    spin: Optional[float] = 0.0
    zone_location: Optional[int] = 0
    sz_top: Optional[float] = 0.0
    sz_bot: Optional[float] = 0.0
    pfx_x: Optional[float] = 0.0
    pfx_z: Optional[float] = 0.0
    px: Optional[float] = 0.0
    pz: Optional[float] = 0.0
    pxold: Optional[float] = 0.0
    pzold: Optional[float] = 0.0

    class Config:
        orm_mode = True
