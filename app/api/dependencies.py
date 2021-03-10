from datetime import datetime
from fastapi import Query, Depends, HTTPException
from vigorish.app import Vigorish
from vigorish.database import Season
from vigorish.enums import TeamID

from app.core.database import get_vig_app


class MLBSeason:
    def __init__(self, year: int = Query(..., ge=2017, le=2019), app: Vigorish = Depends(get_vig_app)):
        season = Season.find_by_year(app.db_session, year)
        if not season:
            raise HTTPException(status_code=404, detail="No results found")
        self.year = season.year
        self.start_date = season.start_date
        self.end_date = season.end_date
        self.asg_date = season.asg_date


class MLBGameDate:
    def __init__(
        self,
        year: MLBSeason = Depends(),
        month: int = Query(..., ge=1, le=12),
        day: int = Query(..., ge=1, le=31),
        app: Vigorish = Depends(get_vig_app),
    ):
        try:
            parsed_date = datetime(year.year, month, day)
        except ValueError:
            raise HTTPException(status_code=404, detail="No results found")
        result = Season.is_date_in_season(app.db_session, parsed_date)
        if result.failure:
            raise HTTPException(status_code=404, detail="No results found")
        self.date = parsed_date


class TeamParameters:
    def __init__(self, team_id: TeamID = Query(..., alias="team-id"), year: MLBSeason = Depends()):
        self.team_id = team_id.name
        self.year = year.year
