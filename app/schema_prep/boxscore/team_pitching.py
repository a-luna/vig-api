def create_team_pitching_stats_html_table(team_pitching_data):
    return [
        create_html_row(row_id, player_pitch_stats)
        for (row_id, player_pitch_stats) in enumerate(team_pitching_data.values(), start=1)
    ]


def create_html_row(row_id, player_pitch_stats):
    return {
        "row_id": row_id,
        "name": player_pitch_stats["name"],
        "mlb_id": player_pitch_stats["mlb_id"],
        "pitch_app_type": player_pitch_stats["pitch_app_type"],
        "stat_line": player_pitch_stats["game_results"],
        "pitch_app_id": player_pitch_stats["pitch_app_id"],
        "innings_pitched": player_pitch_stats["bbref_data"]["innings_pitched"],
        "hits": player_pitch_stats["bbref_data"]["hits"],
        "runs": player_pitch_stats["bbref_data"]["runs"],
        "earned_runs": player_pitch_stats["bbref_data"]["earned_runs"],
        "bases_on_balls": player_pitch_stats["bbref_data"]["bases_on_balls"],
        "strikeouts": player_pitch_stats["bbref_data"]["strikeouts"],
        "homeruns": player_pitch_stats["bbref_data"]["homeruns"],
        "batters_faced": player_pitch_stats["bbref_data"]["batters_faced"],
        "pitch_count": player_pitch_stats["bbref_data"]["pitch_count"],
        "strikes": player_pitch_stats["bbref_data"]["strikes"],
        "strikes_contact": player_pitch_stats["bbref_data"]["strikes_contact"],
        "strikes_swinging": player_pitch_stats["bbref_data"]["strikes_swinging"],
        "strikes_looking": player_pitch_stats["bbref_data"]["strikes_looking"],
        "ground_balls": player_pitch_stats["bbref_data"]["ground_balls"],
        "fly_balls": player_pitch_stats["bbref_data"]["fly_balls"],
        "line_drives": player_pitch_stats["bbref_data"]["line_drives"],
        "unknown_type": player_pitch_stats["bbref_data"]["unknown_type"],
        "game_score": player_pitch_stats["bbref_data"]["game_score"],
        "inherited_runners": player_pitch_stats["bbref_data"]["inherited_runners"],
        "inherited_scored": player_pitch_stats["bbref_data"]["inherited_scored"],
        "wpa_pitch": player_pitch_stats["bbref_data"]["wpa_pitch"],
        "avg_lvg_index": player_pitch_stats["bbref_data"]["avg_lvg_index"],
        "re24_pitch": player_pitch_stats["bbref_data"]["re24_pitch"],
        "at_bat_ids": player_pitch_stats["at_bat_ids"],
        "inning_totals": player_pitch_stats["inning_totals"],
        "substitutions": player_pitch_stats["substitutions"],
    }
