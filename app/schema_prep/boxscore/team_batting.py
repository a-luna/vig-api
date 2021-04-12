import re
from collections import defaultdict

from vigorish.enums import DefensePosition
from vigorish.util.list_helpers import flatten_list2d

PLAYER_SUB_POS_CHANGE_REGEX = re.compile(
    r"""
    from\s
    \b(?P<old_pos>[123BCFHLNPRS]{1,2})\b
    \sto\s
    \b(?P<new_pos>[123BCFHLNPRS]{1,2})\b
""",
    re.VERBOSE,
)


def create_team_batting_stats_html_table(team_batting_data):
    html_rows = []
    sub_tracker = defaultdict(int)
    for player_bat_stats in team_batting_data.values():
        (html_row, sub_tracker) = create_html_row(player_bat_stats, sub_tracker)
        html_rows.append(html_row)
    return sorted(html_rows, key=lambda x: x["row_id"])


def create_html_row(player_bat_stats, sub_tracker):
    row_id = player_bat_stats["bat_order"] * 10
    bat_order = player_bat_stats["bat_order"]
    def_position = player_bat_stats["def_position"]
    position_start = str(DefensePosition(player_bat_stats["def_position"]))
    position_changes = find_position_changes(player_bat_stats, position_start)
    at_bats_str = player_bat_stats["at_bats"]
    bat_stats = player_bat_stats["bat_stats"]
    stat_line = f"{at_bats_str} ({bat_stats})" if bat_stats else at_bats_str
    if not player_bat_stats["is_starter"]:
        sub_entry_info = player_bat_stats["substitutions"][0]
        sub_tracker[sub_entry_info["lineup_slot"]] += 1
        row_id = sub_entry_info["lineup_slot"] * 10 + sub_tracker[sub_entry_info["lineup_slot"]]
        bat_order = sub_entry_info["lineup_slot"]
        position_start = sub_entry_info["incoming_player_pos"]

    html_row = {
        "row_id": row_id,
        "name": player_bat_stats["name"],
        "mlb_id": player_bat_stats["mlb_id"],
        "is_starter": player_bat_stats["is_starter"],
        "bat_order": bat_order,
        "def_position": def_position,
        "position_start": position_start,
        "position_changes": position_changes,
        "stat_line": stat_line,
        "plate_appearances": player_bat_stats["bbref_data"]["plate_appearances"],
        "at_bats": player_bat_stats["bbref_data"]["at_bats"],
        "hits": player_bat_stats["bbref_data"]["hits"],
        "runs_scored": player_bat_stats["bbref_data"]["runs_scored"],
        "rbis": player_bat_stats["bbref_data"]["rbis"],
        "bases_on_balls": player_bat_stats["bbref_data"]["bases_on_balls"],
        "strikeouts": player_bat_stats["bbref_data"]["strikeouts"],
        "avg_to_date": player_bat_stats["bbref_data"]["avg_to_date"],
        "obp_to_date": player_bat_stats["bbref_data"]["obp_to_date"],
        "slg_to_date": player_bat_stats["bbref_data"]["slg_to_date"],
        "ops_to_date": player_bat_stats["bbref_data"]["ops_to_date"],
        "total_pitches": player_bat_stats["bbref_data"]["total_pitches"],
        "total_strikes": player_bat_stats["bbref_data"]["total_strikes"],
        "wpa_bat": player_bat_stats["bbref_data"]["wpa_bat"],
        "avg_lvg_index": player_bat_stats["bbref_data"]["avg_lvg_index"],
        "wpa_bat_pos": player_bat_stats["bbref_data"]["wpa_bat_pos"],
        "wpa_bat_neg": player_bat_stats["bbref_data"]["wpa_bat_neg"],
        "re24_bat": player_bat_stats["bbref_data"]["re24_bat"],
        "details": player_bat_stats["bbref_data"]["details"],
        "at_bat_ids": player_bat_stats["at_bat_ids"],
        "incomplete_at_bat_ids": player_bat_stats["incomplete_at_bat_ids"],
        "substitutions": player_bat_stats["substitutions"],
    }
    return (html_row, sub_tracker)


def find_position_changes(player_bat_stats, position_start):
    if not player_bat_stats["substitutions"]:
        return position_start
    search_results = [
        PLAYER_SUB_POS_CHANGE_REGEX.search(sub_event["sub_description"])
        for sub_event in player_bat_stats["substitutions"]
    ]
    is_starter = player_bat_stats["is_starter"]
    position_changes = flatten_list2d([list(match.groups()) for match in search_results if match])
    incoming_player_pos = player_bat_stats["substitutions"][0]["incoming_player_pos"]
    outgoing_player_pos = player_bat_stats["substitutions"][0]["outgoing_player_pos"]
    return (
        "-".join(position_changes) if position_changes else outgoing_player_pos if is_starter else incoming_player_pos
    )
