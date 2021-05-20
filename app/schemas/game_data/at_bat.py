from datetime import datetime
from typing import List, Union

from pydantic import BaseModel
from vigorish.util.dt_format_strings import DT_AWARE


class AtBatEvent(BaseModel):
    inning_id: str
    inning_label: str
    pbp_table_row_number: int
    at_bat_id: str
    event_type: str


class PlayByPlayEvent(AtBatEvent):
    event_id: str
    score: str
    outs_before_play: int
    runners_on_base: str
    pitch_sequence: str
    runs_outs_result: str
    team_batting_id_br: str
    team_pitching_id_br: str
    play_description: str
    pitcher_id_br: str
    batter_id_br: str
    is_complete_at_bat: bool


class PlayerSubEvent(AtBatEvent):
    sub_type: str
    team_id: str
    sub_description: str
    outgoing_player_id_br: str
    outgoing_player_pos: str
    incoming_player_id_br: str
    incoming_player_pos: str
    lineup_slot: int


class MiscGameEvent(AtBatEvent):
    description: str


class AtBatSchema(BaseModel):
    at_bat_id: str
    pfx_ab_id: int
    inning_id: str
    inning_label: str
    pitch_app_id: str
    pbp_table_row_number: int
    pitcher_id_bbref: str
    pitcher_id_mlb: int
    pitcher_name: str
    pitcher_throws: str
    batter_id_bbref: str
    batter_id_mlb: int
    batter_name: str
    batter_stance: str
    since_game_start: int
    at_bat_duration: int
    is_complete_at_bat: bool
    score: str
    outs_before_play: int
    runners_on_base: str
    runs_outs_result: str
    play_description: str
    total_pitches: int
    pfx_complete: bool
    pfx_des: str
    final_count_balls: int
    final_count_strikes: int
    pitch_sequence_description: List[List[str]]
    pbp_events: List[Union[PlayByPlayEvent, PlayerSubEvent, MiscGameEvent]]
    first_pitch_thrown: str = None
    last_pitch_thrown: str = None

    @property
    def first_pitch_thrown_at(self):
        return datetime.strptime(self.first_pitch_thrown, DT_AWARE) if self.first_pitch_thrown else None

    @property
    def last_pitch_thrown_at(self):
        return datetime.strptime(self.last_pitch_thrown, DT_AWARE) if self.last_pitch_thrown else None
