from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from vigorish.enums import PitchType


class BatterPercentiles(BaseModel):
    bb_rate: Tuple[float, float]
    k_rate: Tuple[float, float]
    contact_rate: Tuple[float, float]
    o_swing_rate: Tuple[float, float]
    whiff_rate: Tuple[float, float]
    bad_whiff_rate: Tuple[float, float]
    line_drive_rate: Tuple[float, float]
    barrel_rate: Tuple[float, float]
    avg_launch_speed: Tuple[float, float]
    max_launch_speed: Tuple[float, float]


class PitchTypePercentilesSchema(BaseModel):
    pitch_type: Union[str, PitchType]
    avg_speed: Tuple[float, float]
    ops: Tuple[float, float]
    zone_rate: Tuple[float, float]
    o_swing_rate: Tuple[float, float]
    whiff_rate: Tuple[float, float]
    bad_whiff_rate: Tuple[float, float]
    contact_rate: Tuple[float, float]
    ground_ball_rate: Tuple[float, float]
    barrel_rate: Tuple[float, float]
    avg_exit_velocity: Tuple[float, float]


class PitchFxMetricsSchema(BaseModel):
    avg: float
    avg_break_angle: float
    avg_break_length: float
    avg_break_y: float
    avg_extension: float
    avg_hit_distance: float
    avg_launch_angle: float
    avg_launch_speed: float
    avg_pfx_x: float
    avg_pfx_z: float
    avg_plate_time: float
    avg_px: float
    avg_pz: float
    avg_speed: float
    avg_spin_direction: float
    avg_spin_rate: float
    bad_whiff_rate: float
    barrel_rate: float
    bb_rate: float
    called_strike_rate: float
    contact_rate: float
    csw_rate: float
    fly_ball_rate: float
    ground_ball_rate: float
    hard_hit_rate: float
    hr_per_fb: float
    iso: float
    k_rate: float
    line_drive_rate: float
    max_launch_speed: float
    medium_hit_rate: float
    mlb_id: Optional[str]
    o_contact_rate: float
    o_swing_rate: float
    obp: float
    ops: float
    percent: float
    pitch_type: List[str]
    pitch_type_int: int
    popup_rate: float
    slg: float
    soft_hit_rate: float
    swing_rate: float
    swinging_strike_rate: float
    total_at_bats: int
    total_bad_whiffs: int
    total_balls_in_play: int
    total_barrels: int
    total_bb: int
    total_called_strikes: int
    total_contact_inside_zone: int
    total_contact_outside_zone: int
    total_doubles: int
    total_errors: int
    total_fly_balls: int
    total_ground_balls: int
    total_hard_hits: int
    total_hbp: int
    total_hits: int
    total_homeruns: int
    total_ibb: int
    total_inside_strike_zone: int
    total_k: int
    total_line_drives: int
    total_medium_hits: int
    total_outs: int
    total_outside_strike_zone: int
    total_pa: int
    total_pitches: int
    total_popups: int
    total_sac_fly: int
    total_sac_hit: int
    total_singles: int
    total_soft_hits: int
    total_swinging_strikes: int
    total_swings: int
    total_swings_inside_zone: int
    total_swings_made_contact: int
    total_swings_outside_zone: int
    total_triples: int
    whiff_rate: float
    z_contact_rate: float
    z_swing_rate: float
    zone_rate: float
    bat_stand: Optional[str] = ""
    p_throws: Optional[str] = ""


class PitchFxMetricsSetSchema(BaseModel):
    pitch_type: List[str]
    pitch_type_int: int
    total_pitches: int
    total_pfx_removed: int
    metrics_combined: PitchFxMetricsSchema
    metrics_by_pitch_type: Dict[str, PitchFxMetricsSchema]


class PitchFxBattingMetricsSchema(BaseModel):
    vs_all: PitchFxMetricsSetSchema
    vs_rhp: PitchFxMetricsSetSchema
    vs_lhp: PitchFxMetricsSetSchema
    as_rhb_vs_rhp: PitchFxMetricsSetSchema
    as_rhb_vs_lhp: PitchFxMetricsSetSchema
    as_lhb_vs_rhp: PitchFxMetricsSetSchema
    as_lhb_vs_lhp: PitchFxMetricsSetSchema


class PitchFxPitchingMetricsSchema(BaseModel):
    all: PitchFxMetricsSetSchema
    rhb: PitchFxMetricsSetSchema
    lhb: PitchFxMetricsSetSchema


class PfxMetricsForPitchTypeSchema(BaseModel):
    metrics: PitchFxMetricsSchema
    percentiles: PitchTypePercentilesSchema


class PfxMetricsByPitchTypeSchema(BaseModel):
    __root__: Dict[str, PfxMetricsForPitchTypeSchema]


class PfxMetricsBySeasonSchema(BaseModel):
    __root__: Dict[int, PfxMetricsByPitchTypeSchema]


class CareerPfxMetricsForPitcherSchema(BaseModel):
    all: PfxMetricsBySeasonSchema
    rhb: PfxMetricsBySeasonSchema
    lhb: PfxMetricsBySeasonSchema
