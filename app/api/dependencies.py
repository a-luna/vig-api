from typing import Optional

from fastapi import Query, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.database import Season
from vigorish.enums import TeamID
from vigorish.util.string_helpers import parse_date, validate_pitch_app_id

from app.core.database import get_vig_app


def get_pitch_app_params(
    game_id: Optional[str] = None, mlb_id: Optional[str] = None, pitch_app_id: Optional[str] = None
):
    if mlb_id and game_id:
        return (mlb_id, game_id)
    if not pitch_app_id:
        raise HTTPException(status_code=400, detail="Must provide pitch_app_id OR game_id and mlb_id query parameters")
    result = validate_pitch_app_id(pitch_app_id)
    if result.failure:
        raise HTTPException(status_code=400, detail=f"{pitch_app_id} is not a valid pitch app ID")
    pitch_app_dict = result.value
    game_id = pitch_app_dict["game_id"]
    mlb_id = pitch_app_dict["pitcher_id"]
    return (mlb_id, game_id)


class BatOrder:
    def __init__(self, bat_order: int = Query(..., ge=0, le=9)):
        self.number = bat_order


class MLBSeason:
    def __init__(self, year: int = Query(..., ge=2017, le=2019), app: Vigorish = Depends(get_vig_app)):
        season = Season.find_by_year(app.db_session, year)
        if not season:
            raise HTTPException(status_code=404, detail="No results found")
        self.year = season.year
        self.start_date = season.start_date
        self.end_date = season.end_date
        self.asg_date = season.asg_date


class MLBDateRange:
    def __init__(
        self,
        start_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
        end_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
        app: Vigorish = Depends(get_vig_app),
    ):
        try:
            start = parse_date(start_date)
            end = parse_date(end_date)
        except ValueError as ex:
            raise HTTPException(status_code=400, detail=ex.message)
        result = Season.is_date_in_season(app.db_session, start)
        if result.failure:
            raise HTTPException(status_code=400, detail=result.error)
        result = Season.is_date_in_season(app.db_session, end)
        if result.failure:
            raise HTTPException(status_code=400, detail=result.error)
        self.start_date = start
        self.end_date = end


class MLBGameDate:
    def __init__(
        self,
        game_date: str = Query(..., description="Date as a string in YYYYMMDD format"),
        app: Vigorish = Depends(get_vig_app),
    ):
        try:
            parsed_date = parse_date(game_date)
        except ValueError as ex:
            raise HTTPException(status_code=400, detail=ex.message)
        result = Season.is_date_in_season(app.db_session, parsed_date)
        if result.failure:
            raise HTTPException(status_code=400, detail=result.error)
        self.date = parsed_date


class TeamParameters:
    def __init__(self, team_id: TeamID, season: MLBSeason = Depends()):
        self.team_id = team_id.name
        self.year = season.year
