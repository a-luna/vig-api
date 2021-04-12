from app.schema_prep.boxscore import (
    create_html_linescore_columns,
    create_team_batting_stats_html_table,
    create_team_pitching_stats_html_table,
)


def convert_boxscore_data(boxscore):
    boxscore["linescore"] = create_html_linescore_columns(boxscore["linescore"])
    if boxscore["extra_innings"]:
        boxscore["linescore_complete"] = create_html_linescore_columns(boxscore["linescore_complete"])
    boxscore["away_team"]["batting"] = create_team_batting_stats_html_table(boxscore["away_team"].pop("batting"))
    boxscore["away_team"]["pitching"] = create_team_pitching_stats_html_table(boxscore["away_team"].pop("pitching"))
    boxscore["home_team"]["batting"] = create_team_batting_stats_html_table(boxscore["home_team"].pop("batting"))
    boxscore["home_team"]["pitching"] = create_team_pitching_stats_html_table(boxscore["home_team"].pop("pitching"))
    return boxscore


def convert_scoreboard_data(scoreboard):
    for num in range(len(scoreboard["games_for_date"])):
        linescore = scoreboard["games_for_date"][num]["linescore"]
        scoreboard["games_for_date"][num]["linescore"] = create_html_linescore_columns(linescore)
    return scoreboard
