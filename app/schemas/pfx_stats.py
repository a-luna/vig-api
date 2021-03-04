from typing import Dict, List, Union

from pydantic import BaseModel
from vigorish.enums import PitchType


class PfxStatsSchema(BaseModel):
    pitcher_id_mlb: int
    pitch_type: Union[PitchType, List[PitchType]]
    total_pitches: int
    total_pa: int
    total_at_bats: int
    total_outs: int
    total_hits: int
    total_bb: int
    total_k: int
    avg_speed: float
    avg: float
    obp: float
    slg: float
    ops: float
    iso: float
    fly_ball_rate: float
    ground_ball_rate: float
    line_drive_rate: float
    pop_up_rate: float
    bb_rate: float
    k_rate: float
    hr_per_fb: float
    avg_pfx_x: float
    avg_pfx_z: float
    avg_px: float
    avg_pz: float
    zone_rate: float
    called_strike_rate: float
    swinging_strike_rate: float
    whiff_rate: float
    csw_rate: float
    o_swing_rate: float
    z_swing_rate: float
    swing_rate: float
    o_contact_rate: float
    z_contact_rate: float
    contact_rate: float
    custom_score: float
    money_pitch: bool
    total_swings: int
    total_swings_made_contact: int
    total_called_strikes: int
    total_swinging_strikes: int
    total_inside_strike_zone: int
    total_outside_strike_zone: int
    total_swings_inside_zone: int
    total_swings_outside_zone: int
    total_contact_inside_zone: int
    total_contact_outside_zone: int
    total_batted_balls: int
    total_ground_balls: int
    total_line_drives: int
    total_fly_balls: int
    total_pop_ups: int
    total_singles: int
    total_doubles: int
    total_triples: int
    total_homeruns: int
    total_ibb: int
    total_hbp: int
    total_errors: int
    total_sac_hit: int
    total_sac_fly: int
    pitch_type_int: int
    percent: float


class PfxStatsCollectionSchema(PfxStatsSchema):
    pitch_type_metrics: Dict[PitchType, PfxStatsSchema]
