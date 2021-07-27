from typing import Dict, List, Tuple, Union

from halo import Halo
from sqlalchemy import func
from sqlalchemy.orm import load_only
from vigorish.cli.components.util import get_random_cli_color, get_random_dots_spinner

import vigorish.database as db
from vigorish.app import Vigorish
from vigorish.enums import DefensePosition
from vigorish.util.list_helpers import group_and_sort_list


def define_all_player_team_roles(app):
    orphaned_ids = []
    spinner = Halo(spinner=get_random_dots_spinner(), color=get_random_cli_color())
    spinner.text = "Creating player ID set...."
    spinner.start()
    all_player_ids = get_all_player_ids(app)
    spinner.text = f"0% Complete 0/{len(all_player_ids)}"
    for num, pid in enumerate(all_player_ids, start=1):
        player = app.db_session.query(db.Player).get(pid)
        if not player:
            orphaned_ids.append(pid)
            continue
        player_teams = (
            app.db_session.query(db.Assoc_Player_Team)
            .filter_by(db_player_id=player.id)
            .filter_by(role_is_defined=0)
            .filter(db.Assoc_Player_Team.year >= 2017)
            .all()
        )
        percent = num / float(len(all_player_ids))
        spinner.text = f"{percent:.0%} Complete {num}/{len(all_player_ids)} Now: {player.name_first} {player.name_last}"
        for team_assoc in player_teams:
            bat_pitch_stats = get_number_of_batting_stats_and_pitching_stats(app, team_assoc)
            spinner.text = (
                f"{percent:.0%} Complete {num}/{len(all_player_ids)} Now: {player.name_first} {player.name_last} "
                f"({team_assoc.team_id} {team_assoc.year})"
            )
            if not bat_pitch_stats["bat_percent"] and not bat_pitch_stats["pitch_percent"]:
                team_assoc.relief_pitcher = 0
                team_assoc.starting_pitcher = 0
                team_assoc.starting_lineup = 0
                team_assoc.bench_player = 0
                team_assoc.def_pos_list = ""
                team_assoc.role_is_defined = 0
                continue
            player_type = determine_if_player_is_batter_or_pitcher(bat_pitch_stats)
            if player_type == "bat":
                pos_counts = get_def_positions_played_by_batter(app, team_assoc)
                determine_if_player_is_starter_or_bench_player(pos_counts, team_assoc)
            else:
                pitch_counts = get_all_pitching_stats(app, team_assoc)
                determine_if_pitcher_is_sp_or_rp(pitch_counts, team_assoc)
    app.db_session.commit()
    spinner.stop()
    if orphaned_ids:
        print(f"The following ids were faulty, no record in the player table corresponds to these:\n{orphaned_ids}")


def get_all_player_ids(app: Vigorish) -> List[int]:
    records = app.db_session.query(db.PitchStats).options(load_only(db.PitchStats.player_id)).distinct().all()
    distinct_pids = [records[0].player_id if len(records) == 1 else record.player_id for record in records]
    records = app.db_session.query(db.BatStats).options(load_only(db.BatStats.player_id)).distinct().all()
    distinct_bids = [records[0].player_id if len(records) == 1 else record.player_id for record in records]
    return list(set(distinct_pids + distinct_bids))


def get_number_of_batting_stats_and_pitching_stats(
    app: Vigorish, team_assoc: db.Assoc_Player_Team
) -> Dict[str, Union[int, float]]:
    bat_stats_query = (
        app.db_session.query(db.BatStats)
        .filter_by(player_id=team_assoc.db_player_id)
        .filter_by(player_team_id=team_assoc.db_team_id)
    )
    pitch_stats_query = (
        app.db_session.query(db.PitchStats)
        .filter_by(player_id=team_assoc.db_player_id)
        .filter_by(player_team_id=team_assoc.db_team_id)
    )
    bat_stats_count = get_total_number_of_rows(bat_stats_query)
    pitch_stats_count = get_total_number_of_rows(pitch_stats_query)
    total_stats_count = bat_stats_count + pitch_stats_count
    return {
        "bat_percent": bat_stats_count / float(total_stats_count) if total_stats_count else 0.0,
        "bat_total": bat_stats_count,
        "pitch_percent": pitch_stats_count / float(total_stats_count) if total_stats_count else 0.0,
        "pitch_total": pitch_stats_count,
    }


def get_total_number_of_rows(query) -> int:
    count_q = query.statement.with_only_columns([func.count()]).order_by(None)
    return query.session.execute(count_q).scalar()


def get_def_positions_played_by_batter(
    app: Vigorish, team_assoc: db.Assoc_Player_Team
) -> List[Tuple[DefensePosition, int]]:
    all_bat_stats = (
        app.db_session.query(db.BatStats)
        .filter_by(player_id=team_assoc.db_player_id)
        .filter_by(player_team_id=team_assoc.db_team_id)
        .all()
    )
    bat_stats_grouped = group_and_sort_list(all_bat_stats, "def_position", "date_id")
    pos_counts = [get_pos_metrics(k, v, all_bat_stats) for k, v in bat_stats_grouped.items()]
    return sorted(pos_counts, key=lambda x: x["percent"], reverse=True)


def get_pos_metrics(
    pos_number: str, pos_stats: db.BatStats, player_stats: db.BatStats
) -> Dict[str, Union[bool, int, float, DefensePosition]]:
    def_pos = DefensePosition(int(pos_number))
    return {
        "def_pos": def_pos,
        "is_starter": def_pos.is_starter,
        "total_games": len(pos_stats),
        "percent": round(len(pos_stats) / float(len(player_stats)), 3) * 100,
    }


def determine_if_player_is_batter_or_pitcher(bat_stats_dict):
    return "bat" if bat_stats_dict["bat_percent"] > bat_stats_dict["pitch_percent"] else "pitch"


def determine_if_player_is_starter_or_bench_player(pos_counts: Dict, team_assoc: db.Assoc_Player_Team):
    total_games_as_starter = sum(pos["total_games"] for pos in pos_counts if pos["is_starter"])
    total_games_bench_player = sum(pos["total_games"] for pos in pos_counts if not pos["is_starter"])
    if total_games_as_starter > total_games_bench_player:
        team_assoc.starting_lineup = 1
        team_assoc.bench_player = 0
        team_assoc.def_pos_list = get_pos_list(pos_counts)
    else:
        team_assoc.bench_player = 1
        team_assoc.starting_lineup = 0
        team_assoc.def_pos_list = get_pos_list(pos_counts) or "BN"
    team_assoc.starting_pitcher = 0
    team_assoc.relief_pitcher = 0
    team_assoc.role_is_defined = 1


def get_pos_list(pos_counts):
    pos_list = [
        str(p["def_pos"])
        for p in pos_counts
        if p["percent"] > 0.05
        and p["def_pos"]
        not in [
            DefensePosition.BENCH,
            DefensePosition.PINCH_HITTER,
            DefensePosition.PINCH_RUNNER,
            DefensePosition.NONE,
        ]
    ]
    return "/".join(pos_list)


def get_all_pitching_stats(app: Vigorish, team_assoc: db.Assoc_Player_Team):
    all_sp_stats = (
        app.db_session.query(db.PitchStats)
        .filter_by(player_id=team_assoc.db_player_id)
        .filter_by(player_team_id=team_assoc.db_team_id)
        .filter_by(is_sp=1)
    )
    all_rp_stats = (
        app.db_session.query(db.PitchStats)
        .filter_by(player_id=team_assoc.db_player_id)
        .filter_by(player_team_id=team_assoc.db_team_id)
        .filter_by(is_rp=1)
    )
    sp_stats_count = get_total_number_of_rows(all_sp_stats)
    rp_stats_count = get_total_number_of_rows(all_rp_stats)
    total_stats_count = sp_stats_count + rp_stats_count
    return {
        "sp_percent": sp_stats_count / float(total_stats_count) if total_stats_count else 0.0,
        "sp_total": sp_stats_count,
        "rp_percent": rp_stats_count / float(total_stats_count) if total_stats_count else 0.0,
        "rp_total": rp_stats_count,
    }


def determine_if_pitcher_is_sp_or_rp(pitch_counts, team_assoc: db.Assoc_Player_Team):
    if pitch_counts["sp_percent"] > pitch_counts["rp_percent"]:
        team_assoc.starting_pitcher = 1
        team_assoc.relief_pitcher = 0
        team_assoc.def_pos_list = "SP"
    else:
        team_assoc.relief_pitcher = 1
        team_assoc.starting_pitcher = 0
        team_assoc.def_pos_list = "RP"
    team_assoc.starting_lineup = 0
    team_assoc.bench_player = 0
    team_assoc.role_is_defined = 1


def main():
    app = Vigorish()
    define_all_player_team_roles(app)


if __name__ == "__main__":
    main()
