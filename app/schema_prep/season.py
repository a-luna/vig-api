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
