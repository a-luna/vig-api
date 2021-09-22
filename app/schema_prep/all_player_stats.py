import math
from collections import defaultdict
from datetime import date
from typing import List

from vigorish.app import Vigorish
from vigorish.data.metrics.bat_stats import BatStatsMetrics
from vigorish.data.player_data import PlayerData
from vigorish.util.numeric_helpers import getRandomHexString

from app.schema_prep.constants import TEAM_ID_MAP

ROW_ID_LENGTH = 4


def convert_player_team_stats(stats):
    assign_league_and_division_to_team_stats(stats)
    return stats


def convert_career_bat_stats(career_bat_stats: BatStatsMetrics, total_seasons: int):
    stats_dict = career_bat_stats.as_dict()
    stats_dict["age"] = 0
    stats_dict["league"] = "MLB"
    stats_dict["changed_teams_midseason"] = False
    stats_dict["all_stats_for_season"] = False
    stats_dict["all_stats_for_stint"] = False
    stats_dict["career_stats_all_teams"] = True
    stats_dict["career_stats_for_team"] = False
    stats_dict["total_seasons"] = total_seasons
    assign_row_id(stats_dict)
    return stats_dict


def calc_season_bat_stats_for_player(
    app: Vigorish,
    mlb_id: int,
    bat_stats_by_year: List[BatStatsMetrics],
    bat_stats_by_team_by_year: List[BatStatsMetrics],
):
    player_data = PlayerData(app, mlb_id)
    all_teams_played_for = [t["team_id"] for t in player_data.all_teams_played_for if t["team_id"]]
    stats_by_year_grouped = {stats.year: stats for stats in bat_stats_by_year}
    stats_by_team_grouped = defaultdict(list)
    for stats in bat_stats_by_team_by_year:
        stats_by_team_grouped[stats.year].append(stats)
    season_stats = []
    for year, stats_by_team_for_year in stats_by_team_grouped.items():
        if len(stats_by_team_for_year) == 1:
            stats_dict = stats_by_team_for_year[0].as_dict()
            assign_league_and_division_to_team_stats(stats_dict)
            stats_dict["age"] = get_player_age_for_season(player_data, year)
            stats_dict["changed_teams_midseason"] = False
            stats_dict["all_stats_for_season"] = True
            stats_dict["all_stats_for_stint"] = False
            stats_dict["career_stats_all_teams"] = False
            stats_dict["career_stats_for_team"] = False
            assign_row_id(stats_dict)
            season_stats.append(stats_dict)
            continue
        season_stats_dict = stats_by_year_grouped[year].as_dict()
        assign_league_and_division_to_team_stats(season_stats_dict)
        season_stats_dict["year"] = year
        season_stats_dict["age"] = get_player_age_for_season(player_data, year)
        season_stats_dict["player_team_id_bbref"] = "TOT"
        season_stats_dict["changed_teams_midseason"] = True
        season_stats_dict["all_stats_for_season"] = True
        season_stats_dict["all_stats_for_stint"] = False
        season_stats_dict["career_stats_all_teams"] = False
        season_stats_dict["career_stats_for_team"] = False
        assign_row_id(season_stats_dict)
        leagues_this_season = []
        team_stints_this_season = []
        for stats in stats_by_team_for_year:
            if stats.player_team_id_bbref not in all_teams_played_for:
                continue
            team_stats_dict = stats.as_dict()
            assign_league_and_division_to_team_stats(team_stats_dict)
            leagues_this_season.append(team_stats_dict["league"])
            team_stats_dict["year"] = year
            team_stats_dict["age"] = get_player_age_for_season(player_data, year)
            team_stats_dict["changed_teams_midseason"] = True
            team_stats_dict["all_stats_for_season"] = False
            team_stats_dict["all_stats_for_stint"] = True
            team_stats_dict["career_stats_all_teams"] = False
            team_stats_dict["career_stats_for_team"] = False
            assign_row_id(team_stats_dict)
            team_stints_this_season.append(team_stats_dict)
        leagues_this_season = list(set(leagues_this_season))
        season_stats_dict["league"] = "MLB" if len(leagues_this_season) > 1 else leagues_this_season[0]
        season_stats.append(season_stats_dict)
        season_stats.extend(team_stints_this_season)
    return season_stats


def calc_career_bat_stats_for_player(
    app: Vigorish,
    mlb_id: int,
    bat_stats_by_team: List[BatStatsMetrics],
    bat_stats_by_team_by_year: List[BatStatsMetrics],
):
    player_data = PlayerData(app, mlb_id)
    all_teams_played_for = [t["team_id"] for t in player_data.all_teams_played_for if t["team_id"]]
    stats_by_team_grouped = defaultdict(list)
    for stats in bat_stats_by_team_by_year:
        stats_by_team_grouped[stats.player_team_id_bbref].append(stats)
    career_stats = []
    for stats_for_team in bat_stats_by_team:
        team_id = stats_for_team.player_team_id_bbref
        if team_id not in all_teams_played_for:
            continue
        total_seasons = len(stats_by_team_grouped[team_id])
        stats_for_team_dict = stats_for_team.as_dict()
        assign_league_and_division_to_team_stats(stats_for_team_dict)
        stats_for_team_dict["age"] = 0
        stats_for_team_dict["career_stats_all_teams"] = False
        stats_for_team_dict["career_stats_for_team"] = True
        stats_for_team_dict["changed_teams_midseason"] = False
        stats_for_team_dict["all_stats_for_season"] = False
        stats_for_team_dict["all_stats_for_stint"] = False
        stats_for_team_dict["total_seasons"] = total_seasons
        assign_row_id(stats_for_team_dict)
        career_stats.append(stats_for_team_dict)
    career_stats.sort(key=lambda x: x["total_seasons"], reverse=True)
    return career_stats


def assign_league_and_division_to_team_stats(team_stats):
    team_id = team_stats.get("player_team_id_bbref")
    team_stats["league"] = TEAM_ID_MAP[team_id]["league"] if team_id else ""
    team_stats["division"] = TEAM_ID_MAP[team_id]["division"] if team_id else ""


def get_player_age_for_season(player_data: PlayerData, year: int):
    player = player_data.player
    duration = date(year, 6, 30) - date(player.birth_year, player.birth_month, player.birth_day)
    return math.floor(duration.total_seconds() / 60 / 60 / 24 / 365.25)


def assign_row_id(stats_dict):
    stats_dict["row_id"] = getRandomHexString(ROW_ID_LENGTH)
