import math
from collections import OrderedDict, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Union
from uuid import uuid4

from dacite import from_dict
from dateutil import parser

from task_master.util import (
    TZ_NAME,
    TZ_NEW_YORK,
    create_bb_game_id,
    get_bb_pitch_log_url,
    get_game_start_time,
    get_mlb_game_feed,
)
from vigorish.constants import (
    BARREL_MAP,
    PITCH_DES_DID_SWING,
    PITCH_DES_MADE_CONTACT,
    PITCH_DES_SWINGING_STRIKE,
)
from vigorish.scrape.brooks_pitch_logs.models.pitch_logs_for_game import BrooksPitchLogsForGame
from vigorish.scrape.brooks_pitchfx.models.pitchfx_log import BrooksPitchFxLog
from vigorish.util.dt_format_strings import DT_AWARE

PitchFxDict = Dict[str, Union[str, int, float, bool]]
PitchFxDictMap = Dict[int, List[PitchFxDict]]


class PitchFxDataConverter:
    def __init__(self) -> None:
        self.game_feed = {}
        self.bbref_game_id = ""
        self.bb_game_id = ""
        self.game_start_time = None
        self.pitchfx_logs = {}
        self.pitch_count = 0
        self.pitcher_id_name_map = {}
        self.player_id_team_map = {}

    @property
    def mlb_game_id(self) -> int:
        return self.game_feed["gamePk"] if self.game_feed else 0

    @property
    def away_team_id(self) -> str:
        return self.game_feed["gameData"]["teams"]["away"]["teamCode"].upper() if self.game_feed else ""

    @property
    def home_team_id(self) -> str:
        return self.game_feed["gameData"]["teams"]["home"]["teamCode"].upper() if self.game_feed else ""

    def get_brooks_pitchfx_logs_for_game(
        self, game_date: datetime, bbref_game_id: str
    ) -> Tuple[BrooksPitchLogsForGame, List[BrooksPitchFxLog]]:
        self.game_feed = get_mlb_game_feed(game_date, bbref_game_id)
        self.game_start_time = get_game_start_time(self.game_feed)
        self.bbref_game_id = bbref_game_id
        self.bb_game_id = create_bb_game_id(game_date, self.game_feed)
        self.pitchfx_logs = defaultdict(list)
        self.pitch_count = 0
        self.pitcher_id_name_map = {}
        self.player_id_team_map = {}
        for at_bat in self.game_feed["liveData"]["plays"]["allPlays"]:
            self.get_pitchfx_data_for_at_bat(at_bat)
        pitch_logs_for_game = self.create_pitch_logs_for_game()
        pfx_logs_for_game = [
            self.create_brooks_pitchfx_log(pitcher_id) for pitcher_id in self.pitcher_id_name_map.keys()
        ]
        return (pitch_logs_for_game, pfx_logs_for_game)

    def get_pitchfx_data_for_at_bat(self, at_bat: Dict):  # sourcery no-metrics skip: boolean-if-exp-identity
        halfInning = at_bat["about"]["halfInning"]
        pitcher_id = at_bat["matchup"]["pitcher"]["id"]
        pitcher_name = at_bat["matchup"]["pitcher"]["fullName"]
        pitcher_team_id_bb = self.home_team_id if halfInning == "top" else self.away_team_id
        opponent_team_id_bb = self.home_team_id if halfInning == "bottom" else self.away_team_id
        pitch_app_id = f"{self.bbref_game_id}_{pitcher_id}"
        batter_id = at_bat["matchup"]["batter"]["id"]
        self.pitcher_id_name_map[pitcher_id] = pitcher_name
        self.player_id_team_map[pitcher_id] = pitcher_team_id_bb
        self.player_id_team_map[batter_id] = opponent_team_id_bb
        ab_id = at_bat["atBatIndex"]
        ab_result = at_bat["result"].get("event", "")
        pitch_events = [e for e in at_bat["playEvents"] if e["index"] in at_bat["pitchIndex"] and e["isPitch"]]

        for event in pitch_events:
            pitchfx = {
                "pitcher_name": pitcher_name,
                "pitch_app_id": pitch_app_id,
                "pitcher_id": pitcher_id,
                "batter_id": batter_id,
                "pitcher_team_id_bb": pitcher_team_id_bb,
                "opponent_team_id_bb": opponent_team_id_bb,
                "bb_game_id": self.bb_game_id,
                "bbref_game_id": self.bbref_game_id,
                "park_sv_id": get_park_sv_id(event["startTime"], self.home_team_id),
                "play_guid": event.get("playId", str(uuid4())),
                "ab_total": len(pitch_events),
                "ab_count": event["pitchNumber"],
                "ab_id": ab_id,
                "des": ab_result,
                "type": get_event_type(event),
                "id": self.pitch_count,
                "sz_top": event["pitchData"].get("strikeZoneTop", 0.0),
                "sz_bot": event["pitchData"].get("strikeZoneBottom", 0.0),
                "mlbam_pitch_name": event["details"].get("type", {}).get("code", "UN"),
                "zone_location": event["pitchData"].get("zone", 0),
                "stand": at_bat["matchup"]["batSide"]["code"],
                "strikes": event["count"]["strikes"],
                "balls": event["count"]["balls"],
                "p_throws": at_bat["matchup"]["pitchHand"]["code"],
                "pdes": event["details"]["description"],
                "inning": at_bat["about"]["inning"],
                "pfx_x": event["pitchData"]["coordinates"].get("pfxX", 0),
                "pfx_z": event["pitchData"]["coordinates"].get("pfxZ", 0),
                "x0": event["pitchData"]["coordinates"].get("x0", 0),
                "y0": event["pitchData"]["coordinates"].get("y0", 0),
                "z0": event["pitchData"]["coordinates"].get("z0", 0),
                "vx0": event["pitchData"]["coordinates"].get("vX0", 0),
                "vy0": event["pitchData"]["coordinates"].get("vY0", 0),
                "vz0": event["pitchData"]["coordinates"].get("vZ0", 0),
                "ax": event["pitchData"]["coordinates"].get("aX", 0),
                "ay": event["pitchData"]["coordinates"].get("aY", 0),
                "az": event["pitchData"]["coordinates"].get("aZ", 0),
                "start_speed": event["pitchData"].get("startSpeed", 0),
                "px": event["pitchData"]["coordinates"].get("pX", 0),
                "pz": event["pitchData"]["coordinates"].get("pZ", 0),
                "plate_time": event["pitchData"].get("plateTime", 0),
                "extension": event["pitchData"].get("extension", 0),
                "break_angle": event["pitchData"]["breaks"].get("breakAngle", 0),
                "break_length": event["pitchData"]["breaks"].get("breakLength", 0),
                "break_y": event["pitchData"]["breaks"].get("breakY", 0),
                "spin_rate": event["pitchData"]["breaks"].get("spinRate", 0),
                "spin_direction": event["pitchData"]["breaks"].get("spinDirection", 0),
                "game_start_time_str": self.game_start_time.strftime(DT_AWARE),
                "time_pitch_thrown_str": get_pitch_thrown_time_localized(event).strftime(DT_AWARE),
                "has_zone_location": True if "zone" in event["pitchData"] else False,
                "batter_did_swing": batter_did_swing(event),
                "batter_made_contact": batter_made_contact(event),
                "called_strike": "Called Strike" in event["details"]["description"],
                "swinging_strike": event["details"]["description"] in PITCH_DES_SWINGING_STRIKE,
                "inside_strike_zone": inside_strike_zone(event),
                "outside_strike_zone": not inside_strike_zone(event),
                "swing_inside_zone": batter_did_swing(event) and inside_strike_zone(event),
                "swing_outside_zone": batter_did_swing(event) and not inside_strike_zone(event),
                "contact_inside_zone": batter_made_contact(event) and inside_strike_zone(event),
                "contact_outside_zone": batter_made_contact(event) and not inside_strike_zone(event),
            }
            if event["details"]["isInPlay"]:
                coordinates = event["hitData"].get("coordinates", {})
                pitchfx["launch_speed"] = event["hitData"].get("launchSpeed", 0)
                pitchfx["launch_angle"] = event["hitData"].get("launchAngle", 0)
                pitchfx["total_distance"] = event["hitData"].get("totalDistance", 0)
                pitchfx["trajectory"] = event["hitData"].get("trajectory", "")
                pitchfx["hardness"] = event["hitData"].get("hardness", "")
                pitchfx["location"] = int(event["hitData"].get("location", "0"))
                pitchfx["coord_x"] = coordinates.get("coordX", 0)
                pitchfx["coord_y"] = coordinates.get("coordY", 0)
                pitchfx["is_in_play"] = True
                pitchfx["is_ground_ball"] = "ground_ball" in event["hitData"].get("trajectory", "")
                pitchfx["is_fly_ball"] = "fly_ball" in event["hitData"].get("trajectory", "")
                pitchfx["is_line_drive"] = "line_drive" in event["hitData"].get("trajectory", "")
                pitchfx["is_popup"] = "popup" in event["hitData"].get("trajectory", "")
                pitchfx["is_hard_hit"] = "hard" in event["hitData"].get("hardness", "")
                pitchfx["is_medium_hit"] = "medium" in event["hitData"].get("hardness", "")
                pitchfx["is_soft_hit"] = "soft" in event["hitData"].get("hardness", "")
                pitchfx["is_barreled"] = is_barreled(event)
            self.pitchfx_logs[pitcher_id].append(pitchfx)
            self.pitch_count += 1

    def create_pitch_logs_for_game(self) -> BrooksPitchLogsForGame:
        pitch_logs = [self.create_pitch_log_for_pitch_app(pitcher_id) for pitcher_id in self.pitcher_id_name_map.keys()]

        pitch_logs_for_game = {
            "bb_game_id": self.bb_game_id,
            "bbref_game_id": self.bbref_game_id,
            "pitch_log_count": str(len(pitch_logs)),
            "pitch_logs": pitch_logs,
        }
        return from_dict(data_class=BrooksPitchLogsForGame, data=pitch_logs_for_game)

    def create_pitch_log_for_pitch_app(self, pitcher_id: int) -> Dict:
        pfx_log = self.pitchfx_logs[pitcher_id]
        pitch_count_by_inning = {
            str(inning): pitch_count for inning, pitch_count in get_pitch_count_by_inning(pfx_log).items()
        }
        pitcher_team_id = self.player_id_team_map[pitcher_id]
        opponent_team_id = self.away_team_id if pitcher_team_id == self.home_team_id else self.home_team_id

        return {
            "parsed_all_info": True,
            "pitcher_name": self.pitcher_id_name_map[pitcher_id],
            "pitcher_id_mlb": pitcher_id,
            "pitch_app_id": f"{self.bbref_game_id}_{pitcher_id}",
            "total_pitch_count": len(pfx_log),
            "pitch_count_by_inning": pitch_count_by_inning,
            "pitcher_team_id_bb": pitcher_team_id,
            "opponent_team_id_bb": opponent_team_id,
            "mlb_game_id": str(self.mlb_game_id),
            "bb_game_id": self.bb_game_id,
            "bbref_game_id": self.bbref_game_id,
            "game_date_year": str(self.game_start_time.year),
            "game_date_month": str(self.game_start_time.month),
            "game_date_day": str(self.game_start_time.day),
            "game_time_hour": str(self.game_start_time.hour),
            "game_time_minute": str(self.game_start_time.minute),
            "time_zone_name": TZ_NAME,
            "pitchfx_url": create_pitchfx_url(pitcher_id, self.mlb_game_id),
            "pitch_log_url": get_bb_pitch_log_url(self.game_start_time, self.mlb_game_id, pitcher_id),
        }

    def create_brooks_pitchfx_log(self, pitcher_id: int) -> BrooksPitchFxLog:
        pfx_log = self.pitchfx_logs[pitcher_id]
        pitcher_team_id = self.player_id_team_map[pitcher_id]
        opponent_team_id = self.away_team_id if pitcher_team_id == self.home_team_id else self.home_team_id

        pfx_log = {
            "pitchfx_log": pfx_log,
            "pitch_count_by_inning": get_pitch_count_by_inning(pfx_log),
            "pitcher_name": self.pitcher_id_name_map[pitcher_id],
            "pitcher_id_mlb": str(pitcher_id),
            "pitch_app_id": f"{self.bbref_game_id}_{pitcher_id}",
            "total_pitch_count": str(len(pfx_log)),
            "pitcher_team_id_bb": pitcher_team_id,
            "opponent_team_id_bb": opponent_team_id,
            "mlb_game_id": str(self.mlb_game_id),
            "bb_game_id": self.bb_game_id,
            "bbref_game_id": self.bbref_game_id,
            "game_date_year": str(self.game_start_time.year),
            "game_date_month": str(self.game_start_time.month),
            "game_date_day": str(self.game_start_time.day),
            "game_time_hour": str(self.game_start_time.hour),
            "game_time_minute": str(self.game_start_time.minute),
            "time_zone_name": TZ_NAME,
            "pitchfx_url": create_pitchfx_url(pitcher_id, self.mlb_game_id),
        }
        return from_dict(data_class=BrooksPitchFxLog, data=pfx_log)


def get_park_sv_id(thrown_at_str: str, home_team_id: str) -> str:
    thrown_at = parser.parse(thrown_at_str)
    return (
        f"{str(thrown_at.year)[-2:]}"
        f"{str(thrown_at.month).zfill(2)}"
        f"{str(thrown_at.day).zfill(2)}_"
        f"{str(thrown_at.hour).zfill(2)}"
        f"{str(thrown_at.minute).zfill(2)}"
        f"{str(thrown_at.second).zfill(2)}"
        f"{home_team_id.lower()}"
    )


def get_event_type(event: Dict) -> str:
    if event["details"]["isInPlay"]:
        return "X"
    if event["details"]["isStrike"]:
        return "S"
    if event["details"]["isBall"]:
        return "B"
    return "Z"


def get_pitch_thrown_time_localized(event: Dict) -> datetime:
    return parser.parse(event["startTime"]).astimezone(TZ_NEW_YORK)


def batter_did_swing(event: Dict) -> bool:
    return event["details"]["description"] in PITCH_DES_DID_SWING


def batter_made_contact(event: Dict) -> bool:
    return event["details"]["description"] in PITCH_DES_MADE_CONTACT


def inside_strike_zone(event: Dict) -> bool:
    posX = 0.70833
    negX = -0.70833
    posZ = event["pitchData"]["strikeZoneTop"]
    negZ = event["pitchData"]["strikeZoneBottom"]
    pX = event["pitchData"]["coordinates"].get("pX", 0)
    pZ = event["pitchData"]["coordinates"].get("pZ", 0)
    return pX < posX and pX > negX and pZ < posZ and pZ > negZ


def is_barreled(event: Dict) -> bool:
    exit_velocity = event["hitData"].get("launchSpeed", 0)
    launch_angle = event["hitData"].get("launchAngle", 0)
    if math.floor(exit_velocity) not in BARREL_MAP:
        return False
    barrel_range = BARREL_MAP.get(math.floor(exit_velocity))
    return launch_angle >= barrel_range["min"] and launch_angle <= barrel_range["max"]


def get_pitch_count_by_inning(pitchfx_log):
    unordered = defaultdict(int)
    for pfx in pitchfx_log:
        unordered[pfx["inning"]] += 1
    pitch_count_by_inning = OrderedDict()
    for k in sorted(unordered.keys()):
        pitch_count_by_inning[k] = unordered[k]
    return pitch_count_by_inning


def create_pitchfx_url(pitcher_id: int, mlb_game_id: int):
    return (
        "https://www.brooksbaseball.net/pfxVB/tabdel_expanded.php?"
        f"pitchSel={pitcher_id}&"
        f"game={mlb_game_id}&"
        "s_type=3&h_size=700&v_size=500"
    )
