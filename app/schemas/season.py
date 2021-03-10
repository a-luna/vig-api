from datetime import datetime

from pydantic import BaseModel


class SeasonSchema(BaseModel):
    year: int
    start_date: datetime
    end_date: datetime
    asg_date: datetime

    class Config:
        orm_mode = True
