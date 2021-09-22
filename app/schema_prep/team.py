import vigorish.database as db

from app.schema_prep.constants import TEAM_ID_MAP


def convert_team_stats_by_year(stats_by_year):
    for stats in stats_by_year.values():
        stats = convert_team_stats(stats)
    return stats_by_year


def convert_team_stats(db_session, team_stats):
    if isinstance(team_stats, dict):
        for stats in team_stats.values():
            convert_for_api_response(db_session, stats)
    if isinstance(team_stats, list):
        for stats in team_stats:
            convert_for_api_response(db_session, stats)
    return team_stats


def convert_for_api_response(db_session, stats):
    assign_league_and_division_to_team_stats(stats)
    add_player_names_to_team_pitching_stats(db_session, stats)
    return stats


def assign_league_and_division_to_team_stats(team_stats):
    team_stats["league"] = TEAM_ID_MAP[team_stats["player_team_id_bbref"]]["league"]
    team_stats["division"] = TEAM_ID_MAP[team_stats["player_team_id_bbref"]]["division"]


def add_player_names_to_team_pitching_stats(db_session, pitch_stats):
    pitch_stats["player_name"] = ""
    if pitch_stats.get("mlb_id"):
        player_id = db.PlayerId.find_by_mlb_id(db_session, pitch_stats["mlb_id"])
        pitch_stats["player_name"] = player_id.mlb_name if player_id else ""
    return pitch_stats
