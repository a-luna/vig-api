from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas import GameDataSchema


class SeasonSchema(BaseModel):
    year: int
    start_date: datetime
    end_date: datetime
    asg_date: datetime

    class Config:
        orm_mode = True


class ScoreboardSchema(BaseModel):
    season: SeasonSchema
    games_for_date: List[GameDataSchema]