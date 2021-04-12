from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from app.schemas import GameDataSchema


class SeasonSchema(BaseModel):
    year: int
    start_date: Union[datetime, str]
    end_date: Union[datetime, str]
    asg_date: Union[datetime, str]

    class Config:
        orm_mode = True


class ScoreboardSchema(BaseModel):
    season: SeasonSchema
    games_for_date: List[GameDataSchema]
