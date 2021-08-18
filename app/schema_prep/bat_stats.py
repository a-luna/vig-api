from typing import Dict, Union

import vigorish.database as db

from app.schemas import GameBatStatsSchema


def convert_bat_stats(bat_stats: db.BatStats):
    bat_stats_dict = convert_bat_stats_to_dict(bat_stats)
    bat_stats_dict["extra_base_hits"] = calc_extra_base_hits(bat_stats_dict)
    bat_stats_dict["total_bases"] = calc_total_bases(bat_stats_dict)
    bat_stats_dict["stat_line"] = parse_bat_stats_for_game(bat_stats_dict)
    bat_stats_dict["player_name"] = bat_stats.player.name
    return bat_stats_dict


def convert_bat_stats_to_dict(bat_stats: db.BatStats) -> Dict[str, Union[str, int, float]]:
    return GameBatStatsSchema.from_orm(bat_stats).dict()


def calc_extra_base_hits(bat_stats: Dict[str, Union[str, int, float]]) -> str:
    return bat_stats["doubles"] + bat_stats["triples"] + bat_stats["homeruns"]


def calc_total_bases(bat_stats: Dict[str, Union[str, int, float]]) -> str:
    homeruns = bat_stats["homeruns"]
    triples = bat_stats["triples"]
    doubles = bat_stats["doubles"]
    singles = bat_stats["hits"] - homeruns - triples - doubles
    return singles + (2 * doubles) + (3 * triples) + (4 * homeruns)


def parse_bat_stats_for_game(bat_stats: Dict[str, Union[str, int, float]]) -> str:
    if not bat_stats["plate_appearances"]:
        return "0/0"
    at_bats = f"{bat_stats['hits']}/{bat_stats['at_bats']}"
    stats = [at_bats]
    if bat_stats["homeruns"]:
        homeruns = bat_stats["homeruns"] if bat_stats["homeruns"] > 1 else ""
        stats.append(f"{homeruns}HR")
    if bat_stats["triples"]:
        triples = f'{bat_stats["triples"]}-' if bat_stats["triples"] > 1 else ""
        stats.append(f"{triples}3B")
    if bat_stats["doubles"]:
        doubles = f'{bat_stats["doubles"]}-' if bat_stats["doubles"] > 1 else ""
        stats.append(f"{doubles}2B")
    if bat_stats["rbis"]:
        rbis = bat_stats["rbis"] if bat_stats["rbis"] > 1 else ""
        stats.append(f"{rbis}RBI")
    if bat_stats["runs_scored"]:
        runs_scored = bat_stats["runs_scored"] if bat_stats["runs_scored"] > 1 else ""
        stats.append(f"{runs_scored}R")
    if bat_stats["stolen_bases"]:
        stolen_bases = bat_stats["stolen_bases"] if bat_stats["stolen_bases"] > 1 else ""
        sb = f"{stolen_bases}SB"
        if bat_stats["caught_stealing"]:
            cs = bat_stats["caught_stealing"] if bat_stats["caught_stealing"] > 1 else ""
            sb += f" ({cs}CS)"
        stats.append(sb)
    if bat_stats["strikeouts"]:
        strikeouts = bat_stats["strikeouts"] if bat_stats["strikeouts"] > 1 else ""
        stats.append(f"{strikeouts}K")
    if bat_stats["bases_on_balls"]:
        bases_on_balls = bat_stats["bases_on_balls"] if bat_stats["bases_on_balls"] > 1 else ""
        bb = f"{bases_on_balls}BB"
        if bat_stats["intentional_bb"]:
            ibb = bat_stats["intentional_bb"] if bat_stats["intentional_bb"] > 1 else ""
            bb += f" ({ibb}IW)"
        stats.append(bb)
    if bat_stats["hit_by_pitch"]:
        hit_by_pitch = bat_stats["hit_by_pitch"] if bat_stats["hit_by_pitch"] > 1 else ""
        stats.append(f"{hit_by_pitch}HBP")
    if bat_stats["gdp"]:
        gdp = bat_stats["gdp"] if bat_stats["gdp"] > 1 else ""
        stats.append(f"{gdp}GDP")
    if bat_stats["sac_fly"]:
        sac_fly = bat_stats["sac_fly"] if bat_stats["sac_fly"] > 1 else ""
        stats.append(f"{sac_fly}SF")
    if bat_stats["sac_hit"]:
        sac_hit = bat_stats["sac_hit"] if bat_stats["sac_hit"] > 1 else ""
        stats.append(f"{sac_hit}SH")
    return ", ".join(stats)
