def convert_scoreboard_data(scoreboard):
    for num in range(len(scoreboard["games_for_date"])):
        linescore = scoreboard["games_for_date"][num]["linescore"]
        scoreboard["games_for_date"][num]["linescore"] = create_html_linescore_columns(linescore)
    return scoreboard
