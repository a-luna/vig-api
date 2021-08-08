from datetime import datetime
from typing import Dict, Union

import vigorish.database as db
from vigorish.app import Vigorish

from app.schemas import GamePitchStatsSchema


def convert_pitch_stats(pitch_stats: db.PitchStats, app: Vigorish, game_date: datetime):
    pitch_stats_dict = convert_pitch_stats_to_dict(pitch_stats)
    mlb_id = pitch_stats_dict["player_id_mlb"]
    (wins, losses) = app.scraped_data.get_pitcher_record_on_date(mlb_id, game_date)
    pitch_stats_dict["wins"] = wins
    pitch_stats_dict["losses"] = losses
    pitch_stats_dict["saves"] = app.scraped_data.get_pitcher_total_saves_on_date(mlb_id, game_date)
    pitch_stats_dict["full_stat_line"] = parse_full_pitch_app_stats(pitch_stats_dict)
    pitch_stats_dict["summary_stat_line"] = parse_summary_pitch_app_stats(pitch_stats_dict)
    pitch_stats_dict["csw"] = pitch_stats_dict["strikes_swinging"] + pitch_stats_dict["strikes_looking"]
    pitch_stats_dict["player_name"] = pitch_stats.player.name
    return pitch_stats_dict


def convert_pitch_stats_to_dict(pitch_stats: db.Player) -> Dict[str, Union[str, int, float]]:
    return GamePitchStatsSchema.from_orm(pitch_stats).dict()


def parse_full_pitch_app_stats(pitch_stats):
    ip = pitch_stats["innings_pitched"]
    r = pitch_stats["runs"]
    er = pitch_stats["earned_runs"]
    runs = f"{er}ER" if er == r else f"{r}R, {er}ER"
    h = pitch_stats["hits"] if pitch_stats["hits"] != 1 else ""
    bb = pitch_stats["bases_on_balls"] if pitch_stats["bases_on_balls"] != 1 else ""
    k = pitch_stats["strikeouts"] if pitch_stats["strikeouts"] != 1 else ""
    stat_list = [f"{h}H", f"{bb}BB", f"{k}K"]
    details = f", {', '.join(stat_list)}"
    return f"{ip} IP, {runs}{details}"


def parse_summary_pitch_app_stats(pitch_stats):
    ip = pitch_stats["innings_pitched"]
    r = pitch_stats["runs"]
    er = pitch_stats["earned_runs"]
    runs = f"{er}ER" if er == r else f"{r}R, {er}ER"
    stat_list = []
    if pitch_stats["hits"]:
        h = pitch_stats["hits"] if pitch_stats["hits"] > 1 else ""
        stat_list.append(f"{h}H")
    if pitch_stats["strikeouts"]:
        k = pitch_stats["strikeouts"] if pitch_stats["strikeouts"] > 1 else ""
        stat_list.append(f"{k}K")
    if pitch_stats["bases_on_balls"]:
        bb = pitch_stats["bases_on_balls"] if pitch_stats["bases_on_balls"] > 1 else ""
        stat_list.append(f"{bb}BB")
    details = f", {', '.join(stat_list)}" if stat_list else ""
    return f"{ip} IP, {runs}{details}"
