from typing import Dict, List, Union

TeamStatDict = Dict[str, Union[int, float, str]]

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


def convert_team_stats(
    team_stats: Union[List[TeamStatDict], Dict[str, TeamStatDict]]
) -> Union[List[TeamStatDict], Dict[str, TeamStatDict]]:
    if isinstance(team_stats, dict):
        for stats in team_stats.values():
            assign_league_and_division_to_team_stats(stats)
    if isinstance(team_stats, list):
        for stats in team_stats:
            assign_league_and_division_to_team_stats(stats)
    return team_stats


def assign_league_and_division_to_team_stats(team_stats: TeamStatDict) -> TeamStatDict:
    team_stats["league"] = TEAM_ID_MAP[team_stats["team_id_bbref"]]["league"]
    team_stats["division"] = TEAM_ID_MAP[team_stats["team_id_bbref"]]["division"]
