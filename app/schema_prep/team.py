import vigorish.database as db

TEAM_ID_MAP = {
    "ARI": {"league": "NL", "division": "W"},
    "ATL": {"league": "NL", "division": "E"},
    "BAL": {"league": "AL", "division": "E"},
    "BOS": {"league": "AL", "division": "E"},
    "CHW": {"league": "AL", "division": "C"},
    "CHC": {"league": "NL", "division": "C"},
    "CIN": {"league": "NL", "division": "C"},
    "CLE": {"league": "AL", "division": "C"},
    "COL": {"league": "NL", "division": "W"},
    "DET": {"league": "AL", "division": "C"},
    "HOU": {"league": "AL", "division": "W"},
    "KCR": {"league": "AL", "division": "C"},
    "LAA": {"league": "AL", "division": "W"},
    "LAD": {"league": "NL", "division": "W"},
    "MIA": {"league": "NL", "division": "E"},
    "MIL": {"league": "NL", "division": "C"},
    "MIN": {"league": "AL", "division": "C"},
    "NYY": {"league": "AL", "division": "E"},
    "NYM": {"league": "NL", "division": "E"},
    "OAK": {"league": "AL", "division": "W"},
    "PHI": {"league": "NL", "division": "E"},
    "PIT": {"league": "NL", "division": "C"},
    "SDP": {"league": "NL", "division": "W"},
    "SEA": {"league": "AL", "division": "W"},
    "SFG": {"league": "NL", "division": "W"},
    "STL": {"league": "NL", "division": "C"},
    "TBR": {"league": "AL", "division": "E"},
    "TEX": {"league": "AL", "division": "W"},
    "TOR": {"league": "AL", "division": "E"},
    "WSN": {"league": "NL", "division": "E"},
}


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
    team_stats["league"] = TEAM_ID_MAP[team_stats["team_id_bbref"]]["league"]
    team_stats["division"] = TEAM_ID_MAP[team_stats["team_id_bbref"]]["division"]


def add_player_names_to_team_pitching_stats(db_session, pitch_stats):
    player_id = db.PlayerId.find_by_mlb_id(db_session, pitch_stats["mlb_id"])
    pitch_stats["player_name"] = player_id.mlb_name if player_id else ""
    return pitch_stats
