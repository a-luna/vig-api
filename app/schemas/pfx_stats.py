from dataclasses import asdict
from typing import Dict, List, Tuple, Union

from pydantic import BaseModel
from vigorish.enums import PitchType


class PitchTypePercentilesSchema(BaseModel):
    pitch_type: Union[str, PitchType]
    avg_speed: Tuple[float, float]
    ops: Tuple[float, float]
    whiff_rate: Tuple[float, float]
    zone_rate: Tuple[float, float]
    contact_rate: Tuple[float, float]
    o_swing_rate: Tuple[float, float]
    ground_ball_rate: Tuple[float, float]
    barrel_rate: Tuple[float, float]
    avg_exit_velocity: Tuple[float, float]


class PfxStatsSchema(BaseModel):
    mlb_id: int
    avg: float
    obp: float
    slg: float
    ops: float
    iso: float
    fly_ball_rate: float
    ground_ball_rate: float
    line_drive_rate: float
    popup_rate: float
    hard_hit_rate: float
    medium_hit_rate: float
    soft_hit_rate: float
    barrel_rate: float
    avg_launch_speed: float
    avg_launch_angle: float
    avg_hit_distance: float
    bb_rate: float
    k_rate: float
    hr_per_fb: float
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
    total_pitches: int
    total_pa: int
    total_at_bats: int
    total_outs: int
    total_hits: int
    total_bb: int
    total_k: int
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
    total_balls_in_play: int
    total_ground_balls: int
    total_line_drives: int
    total_fly_balls: int
    total_popups: int
    total_hard_hits: int
    total_medium_hits: int
    total_soft_hits: int
    total_barrels: int
    total_singles: int
    total_doubles: int
    total_triples: int
    total_homeruns: int
    total_ibb: int
    total_hbp: int
    total_errors: int
    total_sac_hit: int
    total_sac_fly: int


class PfxBattingStatsCollectionSchema(PfxStatsSchema):
    pitch_types_filtered: List[Union[str, PitchType]]
    pitch_types_all: List[Union[str, PitchType]]
    total_pitches_filtered: int
    total_pitches_all: int
    total_pitches_excluded: int
    pitch_type_metrics: Dict[Union[str, PitchType], PfxStatsSchema]


class PfxPitchingStatsSchema(PfxStatsSchema):
    p_throws: str
    pitch_type: Union[str, PitchType]
    avg_speed: float
    avg_pfx_x: float
    avg_pfx_z: float
    avg_px: float
    avg_pz: float
    avg_plate_time: float
    avg_extension: float
    avg_break_angle: float
    avg_break_length: float
    avg_break_y: float
    avg_spin_rate: float
    avg_spin_direction: float
    percent: float


class PfxPitchingStatsCollectionSchema(PfxStatsSchema):
    pitch_types_filtered: List[Union[str, PitchType]]
    pitch_types_all: List[Union[str, PitchType]]
    total_pitches_filtered: int
    total_pitches_all: int
    total_pitches_excluded: int
    pitch_type_metrics: Dict[Union[str, PitchType], PfxPitchingStatsSchema]


class PfxPitchingStatsWithPercentiles(BaseModel):
    metrics: PfxPitchingStatsCollectionSchema
    percentiles: List[PitchTypePercentilesSchema]


class YearlyPfxPitchingStatsWithPercentiles(BaseModel):
    metrics: Dict[int, PfxPitchingStatsCollectionSchema]
    percentiles: Dict[int, List[PitchTypePercentilesSchema]]


class AllPfxDataWithPercentiles(BaseModel):
    both: PfxPitchingStatsWithPercentiles
    rhb: PfxPitchingStatsWithPercentiles
    lhb: PfxPitchingStatsWithPercentiles


class YearlyPfxDataWithPercentiles(BaseModel):
    both: YearlyPfxPitchingStatsWithPercentiles
    rhb: YearlyPfxPitchingStatsWithPercentiles
    lhb: YearlyPfxPitchingStatsWithPercentiles


def prepare_pfx_response_model(pfx_stats):
    response = asdict(pfx_stats)
    response["pitch_types_filtered"] = deconstruct_pitch_types_from_int(response.pop("pitch_type"))
    response["pitch_types_all"] = deconstruct_pitch_types_from_int(response.pop("pitch_type_int"))
    response["total_pitches_all"] = response["total_pitches"]
    response["total_pitches_filtered"] = 0
    for pitch_type_stats in response["pitch_type_metrics"].values():
        response["total_pitches_filtered"] += pitch_type_stats["total_pitches"]
    response["total_pitches_excluded"] = response["total_pitches_all"] - response["total_pitches_filtered"]
    return response


def deconstruct_pitch_types_from_int(pitch_mix_int):
    return [str(pitch_type) for pitch_type in PitchType if pitch_mix_int & pitch_type == pitch_type]
