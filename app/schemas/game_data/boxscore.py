from typing import List, Optional

from pydantic import BaseModel

from app.schemas import TeamDataMapSchema


class LinescoreColumnSchema(BaseModel):
    col_index: int
    col_header: str
    away_team: str
    home_team: str
    css_class: str
    removed_inning: bool


class PlayerIdsSchema(BaseModel):
    mlb_id: int
    name: str
    team_id: str


class PitcherResultsSchema(BaseModel):
    wp: PlayerIdsSchema
    lp: PlayerIdsSchema
    sv: Optional[PlayerIdsSchema]


class GameDataSchema(BaseModel):
    game_id: str
    linescore: List[LinescoreColumnSchema]
    pitcher_results: PitcherResultsSchema
    extra_innings: bool


class UmpireSchema(BaseModel):
    field_location: str
    umpire_name: str


class GameMetaSchema(BaseModel):
    park_name: str
    field_type: str
    day_night: str
    game_start_time: str
    first_pitch_temperature: int
    first_pitch_precipitation: str
    first_pitch_wind: str
    first_pitch_clouds: str
    game_duration: str
    attendance: int
    umpires: List[UmpireSchema]


class BoxscoreSchema(BaseModel):
    game_id: str
    summary: List[str]
    extra_innings: bool
    linescore: List[LinescoreColumnSchema]
    linescore_complete: Optional[List[LinescoreColumnSchema]] = None
    game_meta: GameMetaSchema
    team_data: TeamDataMapSchema
