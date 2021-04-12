def create_html_linescore_columns(linescore):
    if isinstance(linescore, list):
        linescore = linescore[0]
    (_, removed_inning_map) = get_inning_scored_removed_maps(linescore)
    html_dict_keys = ("col_index", "col_header", "away_team", "home_team", "css_class", "removed_inning")
    team_id_column = (0, "&nbsp;", linescore["away_team_id"], linescore["home_team_id"], "team-id", False)
    html_linescore = [dict(zip(html_dict_keys, team_id_column))]

    total_innings = len(linescore["inning_numbers"])
    inning_col_indices = list(range(1, total_innings + 1))
    inning_css_classes = ["inning-runs-scored" for _ in range(total_innings)]
    inning_columns = zip(
        inning_col_indices,
        linescore["inning_numbers"],
        linescore["away_team_runs_by_inning"],
        linescore["home_team_runs_by_inning"],
        inning_css_classes,
        removed_inning_map,
    )
    html_linescore.extend([dict(zip(html_dict_keys, column)) for column in inning_columns])

    game_total_col_indices = list(range(total_innings + 1, total_innings + 4))
    game_total_css_classes = ["game-total" for _ in range(len(linescore["game_totals"]))]
    removed_inning_false = [False for _ in range(len(linescore["game_totals"]))]
    game_total_columns = zip(
        game_total_col_indices,
        linescore["game_totals"],
        linescore["away_team_totals"],
        linescore["home_team_totals"],
        game_total_css_classes,
        removed_inning_false,
    )
    html_linescore.extend([dict(zip(html_dict_keys, column)) for column in game_total_columns])
    return html_linescore


def get_inning_scored_removed_maps(linescore_tables):
    inning_runs_scored_map = get_inning_runs_scored_map(linescore_tables)
    innings_nobody_scored = list(filter(lambda x: not x["runs_scored"], inning_runs_scored_map))
    innings_somebody_scored = list(filter(lambda x: x["runs_scored"], inning_runs_scored_map))
    removed_innings = []
    if len(innings_somebody_scored) < 9:
        missing_column_count = 9 - len(innings_somebody_scored)
        innings_somebody_scored.extend(innings_nobody_scored[:missing_column_count])
        removed_innings = [inn["inning"] for inn in innings_nobody_scored[missing_column_count:]]
    elif len(innings_somebody_scored) > 9:
        remove_column_count = len(innings_somebody_scored) - 9
        innings_somebody_scored.sort(key=lambda x: x["total_runs_scored"])
        innings_somebody_scored = innings_somebody_scored[remove_column_count:]
        removed_innings = [inn["inning"] for inn in innings_nobody_scored[:remove_column_count]]
    removed_inning_map = []
    for inning_map in inning_runs_scored_map:
        removed_inning_map.append(inning_map["inning"] in removed_innings)
        inning_map["removed_inning"] = inning_map["inning"] in removed_innings
    return (inning_runs_scored_map, removed_inning_map)


def get_inning_runs_scored_map(linescore):
    inning_runs_scored_map = []
    inning_numbers_without_filler = [num for num in linescore["inning_numbers"] if num != ""]
    for i in range(len(inning_numbers_without_filler)):
        inning = linescore["inning_numbers"][i]
        away_team_runs_scored = linescore["away_team_runs_by_inning"][i]
        home_team_runs_scored = linescore["home_team_runs_by_inning"][i]
        inning_somebody_scored = away_team_runs_scored != 0 or home_team_runs_scored != 0
        home_team_runs_int = 0 if isinstance(home_team_runs_scored, str) else home_team_runs_scored
        inning_runs_scored_map.append(
            {
                "runs_scored": inning_somebody_scored,
                "inning": inning,
                "away_runs": away_team_runs_scored,
                "home_runs": home_team_runs_scored,
                "total_runs_scored": away_team_runs_scored + home_team_runs_int,
            }
        )
    return inning_runs_scored_map
