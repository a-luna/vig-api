from dateutil import tz

from vigorish.util.dt_format_strings import DT_NAIVE

TZ_NAME = "America/New_York"
TZ_NEW_YORK = tz.gettz(TZ_NAME)


def convert_pfx_times_to_est(pfx):
    pfx["game_start_time_est"] = pfx["game_start_time_utc"].astimezone(TZ_NEW_YORK).strftime(DT_NAIVE)
    pfx["time_pitch_thrown_est"] = pfx["time_pitch_thrown_utc"].astimezone(TZ_NEW_YORK).strftime(DT_NAIVE)
    return pfx
