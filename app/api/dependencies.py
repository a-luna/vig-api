from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException, Query
from vigorish.app import Vigorish
from vigorish.database import Season
from vigorish.enums import TeamID
from vigorish.util.dt_format_strings import DATE_ONLY
from vigorish.util.string_helpers import parse_date, validate_pitch_app_id

from app.core.database import get_vig_app
from app.schema_prep import convert_season_to_dict


def get_date_range(
    start_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
    end_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        return (start, end)
    except ValueError as ex:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=ex.message)


def get_pitch_app_params(
    game_id: Optional[str] = None, mlb_id: Optional[str] = None, pitch_app_id: Optional[str] = None
):
    if mlb_id and game_id:
        return (mlb_id, game_id)
    if not pitch_app_id:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="Must provide pitch_app_id OR game_id and mlb_id query parameters",
        )
    result = validate_pitch_app_id(pitch_app_id)
    if result.failure:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST), detail=f"{pitch_app_id} is not a valid pitch app ID"
        )
    pitch_app_dict = result.value
    return (pitch_app_dict["pitcher_id"], pitch_app_dict["game_id"])


class MLBSeason:
    def __init__(self, year: int = Query(..., ge=2017, le=2021), app: Vigorish = Depends(get_vig_app)):
        season = Season.find_by_year(app.db_session, year)
        if not season:
            raise HTTPException(status_code=int(HTTPStatus.NOT_FOUND), detail="No results found")
        self.year = season.year
        self.start_date = season.start_date
        self.end_date = season.end_date
        self.asg_date = season.asg_date

    def __str__(self):
        return str(self.year)


class MLBGameDate:
    def __init__(
        self,
        game_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
        app: Vigorish = Depends(get_vig_app),
    ):
        try:
            parsed_date = parse_date(game_date)
        except ValueError as ex:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=ex.message)
        result = Season.is_date_in_season(app.db_session, parsed_date)
        if result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)
        self.date = parsed_date
        self.season = convert_season_to_dict(result.value)

    def __str__(self):
        return self.date.strftime(DATE_ONLY)


class TeamParameters:
    def __init__(self, team_id: TeamID, season: MLBSeason = Depends()):
        self.team_id = team_id.name
        self.year = season.year

    def __str__(self):
        return f"{self.team_id}_{self.year}"
