from datetime import datetime

from pydantic import BaseModel


class PlayerSchema(BaseModel):
    name_first: str
    name_last: str
    name_given: str
    bats: str
    throws: str
    weight: int
    height: int
    debut: datetime
    birth_year: int
    birth_month: int
    birth_day: int
    birth_country: str
    birth_state: str
    birth_city: str
    bbref_id: str
    mlb_id: int

    class Config:
        orm_mode = True


class FuzzySearchResult(BaseModel):
    match: str
    score: int
    result: int
