from typing import Dict, Union

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


def convert_team_bat_stats(team_bat_stats: Dict[str, Union[int, float, str]]) -> Dict[str, Union[int, float, str]]:
    for bat_stats in team_bat_stats.values():
        bat_stats["league"] = TEAM_ID_MAP[bat_stats["team_id_bbref"]]["league"]
        bat_stats["division"] = TEAM_ID_MAP[bat_stats["team_id_bbref"]]["division"]
    return team_bat_stats
