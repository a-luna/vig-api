from typing import Dict, Union

from vigorish.database import Season
from vigorish.util.dt_format_strings import DATE_ONLY


def convert_season_to_dict(season: Season) -> Dict[str, Union[int, str]]:
    return {
        "year": season.year,
        "start_date": season.start_date.strftime(DATE_ONLY),
        "end_date": season.end_date.strftime(DATE_ONLY),
        "asg_date": season.asg_date.strftime(DATE_ONLY),
    }


def create_divisional_standings(team_season_data):
    return {
        "al": {
            "w": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "W", team_season_data),
                key=lambda x: x["losses"],
            ),
            "c": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "C", team_season_data),
                key=lambda x: x["losses"],
            ),
            "e": sorted(
                filter(lambda x: x["league"] == "AL" and x["division"] == "E", team_season_data),
                key=lambda x: x["losses"],
            ),
        },
        "nl": {
            "w": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "W", team_season_data),
                key=lambda x: x["losses"],
            ),
            "c": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "C", team_season_data),
                key=lambda x: x["losses"],
            ),
            "e": sorted(
                filter(lambda x: x["league"] == "NL" and x["division"] == "E", team_season_data),
                key=lambda x: x["losses"],
            ),
        },
    }
