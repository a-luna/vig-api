from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from app.schemas.game_data.team_data import TeamDataSchema


class LinescoreColumnSchema(BaseModel):
    col_index: int
    col_header: str
    away_team: str
    home_team: str
    css_class: str
    removed_inning: bool


class InningsRunsScoredSchema(BaseModel):
    runs_scored: bool
    inning: int
    away_runs: int
    home_runs: int
    total_runs_scored: int
    removed_inning: bool


class LinescoreSchema(BaseModel):
    inning_numbers: List[int]
    game_totals: List[str]
    away_team_id: str
    away_team_runs: List[int]
    away_team_totals: List[int]
    home_team_id: str
    home_team_runs: List[Union[int, str]]
    home_team_totals: List[int]
    extra_innings: bool
    removed_innings: Optional[List[bool]]


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
    linescore: LinescoreSchema
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


class InningTotals(BaseModel):
    inning_total_runs: str
    inning_total_hits: str
    inning_total_errors: str
    inning_total_left_on_base: str
    away_team_runs_after_inning: str
    home_team_runs_after_inning: str


class InningSummary(BaseModel):
    inning_label: str
    begin_inning_summary: str
    end_inning_summary: str
    inning_totals: InningTotals


class BoxscoreSchema(BaseModel):
    last_modified: str
    game_id: str
    away_team: TeamDataSchema
    home_team: TeamDataSchema
    extra_innings: bool
    game_meta: GameMetaSchema
    linescore: LinescoreSchema
    linescore_complete: Optional[LinescoreSchema] = None
    inning_summaries: Dict[str, InningSummary]
