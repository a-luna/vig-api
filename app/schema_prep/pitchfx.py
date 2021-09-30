from datetime import timezone
from typing import List

import vigorish.database as db
from vigorish.util.datetime_util import TIME_ZONE_NEW_YORK
from vigorish.util.dt_format_strings import DT_NAIVE

from app.schemas.pitchfx import PitchFxSchema


def convert_pfx_list(pfx: List[db.PitchFx]) -> List[PitchFxSchema]:
    pfx_dicts = [p.as_dict() for p in pfx]
    return list(map(convert_naive_pfx_times, map(convert_pfx_times_to_est, pfx_dicts)))


def convert_naive_pfx_times(pfx):
    pfx["game_start_time_est"] = (
        pfx["game_start_time_utc"].replace(tzinfo=timezone.utc).astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    )
    pfx["time_pitch_thrown_est"] = (
        pfx["time_pitch_thrown_utc"].replace(tzinfo=timezone.utc).astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    )
    return pfx


def convert_pfx_times_to_est(pfx):
    pfx["game_start_time_est"] = pfx["game_start_time_utc"].astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    pfx["time_pitch_thrown_est"] = pfx["time_pitch_thrown_utc"].astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    return pfx
