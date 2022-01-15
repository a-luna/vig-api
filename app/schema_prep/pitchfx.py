from datetime import timezone
from typing import List

import vigorish.database as db
from vigorish.data.game_data import GameData
from vigorish.app import Vigorish
from vigorish.util.datetime_util import TIME_ZONE_NEW_YORK
from vigorish.util.dt_format_strings import DT_NAIVE

from app.schemas.pitchfx import PitchFxSchema


def convert_pfx_list(app: Vigorish, pfx: List[db.PitchFx]) -> List[PitchFxSchema]:
    pfx_dicts = [p.as_dict() for p in pfx]
    for pfx_dict in pfx_dicts:
        pfx_dict = populate_count(pfx_dict)
        pfx_dict = populate_data_requiring_db(app, pfx_dict)
    return list(map(convert_naive_pfx_times, map(convert_pfx_times_to_est, pfx_dicts)))


def populate_count(pfx: db.PitchFx):
    pfx["count"] = f'{pfx["balls"]}-{pfx["strikes"]}'
    pfx["two_strike_count"] = pfx["strikes"] == 2
    return pfx


def populate_data_requiring_db(app: Vigorish, pfx: db.PitchFx):
    game_data = GameData(app, pfx["bbref_game_id"])
    at_bat_data = game_data.at_bat_map.get(pfx["at_bat_id"], {"runs_outs_result": ""})
    pfx = populate_player_names(at_bat_data, pfx)
    pfx = populate_runs_outs_result(at_bat_data, pfx)
    pfx = populate_pitch_sequence(at_bat_data, pfx)
    pfx = populate_outs_before_play(at_bat_data, pfx)
    pfx = populate_at_bat_outcome(at_bat_data, pfx)
    return pfx


def populate_player_names(at_bat_data: dict, pfx: db.PitchFx):
    pfx["pitcher_name"] = at_bat_data["pitcher_name"]
    pfx["batter_name"] = at_bat_data["batter_name"]
    return pfx


def populate_runs_outs_result(at_bat_data: dict, pfx: db.PitchFx):
    runs_outs_result = at_bat_data.get("runs_outs_result", "")
    pfx["runs_outs_result"] = runs_outs_result
    pfx["runs_scored"] = runs_outs_result.count("R")
    return pfx


def populate_pitch_sequence(at_bat_data: dict, pfx: db.PitchFx):
    pbp_events = [event for event in at_bat_data["pbp_events"] if event["event_type"] == "AT_BAT"]
    pbp_events.sort(key=lambda x: x["pbp_table_row_number"])
    pfx["pitch_sequence"] = pbp_events[-1]["pitch_sequence"]
    return pfx


def populate_outs_before_play(at_bat_data: dict, pfx: db.PitchFx):
    pfx["outs_before_play"] = at_bat_data["outs_before_play"]
    return pfx


def populate_at_bat_outcome(at_bat_data: dict, pfx: db.PitchFx):
    if not pfx["ab_result_hit"]:
        pfx["ab_outcome"] = pfx["pdes"]
        return pfx
    hit_type = (
        "Single"
        if pfx["ab_result_single"]
        else "Double"
        if pfx["ab_result_double"]
        else "Triple"
        if pfx["ab_result_triple"]
        else "Homerun"
        if pfx["ab_result_homerun"]
        else ""
    )
    runs_outs_result = at_bat_data.get("runs_outs_result", "")
    rbi_count = runs_outs_result.count("R")
    if pfx["ab_result_homerun"] and rbi_count == 4:
        pfx["ab_outcome"] = "Grand Slam"
        return pfx
    if rbi_count == 0 or (pfx["ab_result_homerun"] and rbi_count == 1):
        pfx["ab_outcome"] = hit_type
        return pfx
    rbis = f"{rbi_count} RBI" if rbi_count > 1 else "RBI"
    pfx["ab_outcome"] = f"{hit_type} ({rbis})"
    return pfx


def convert_naive_pfx_times(pfx: db.PitchFx):
    pfx["game_start_time_est"] = (
        pfx["game_start_time_utc"].replace(tzinfo=timezone.utc).astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    )
    pfx["time_pitch_thrown_est"] = (
        pfx["time_pitch_thrown_utc"].replace(tzinfo=timezone.utc).astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    )
    return pfx


def convert_pfx_times_to_est(pfx: db.PitchFx):
    pfx["game_start_time_est"] = pfx["game_start_time_utc"].astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    pfx["time_pitch_thrown_est"] = pfx["time_pitch_thrown_utc"].astimezone(TIME_ZONE_NEW_YORK).strftime(DT_NAIVE)
    return pfx
