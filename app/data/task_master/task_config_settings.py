from dataclasses import dataclass, field
from typing import Dict

from vigorish.enums import DataSet, ScrapeCondition


@dataclass
class TaskConfigSettings:
    mlb_season: int = 2021
    reset_db_scrape_status: bool = False
    remove_db_game_data: bool = False
    update_id_map: bool = False
    update_player_team_roles: bool = False
    rescrape_bbref_html: Dict[DataSet, bool] = field(
        default_factory={"BBREF_GAMES_FOR_DATE": False, "BBREF_BOXSCORES": False}
    )
    parse_bbref_html: Dict[DataSet, ScrapeCondition] = field(
        default_factory={
            "BBREF_GAMES_FOR_DATE": ScrapeCondition.ONLY_MISSING_DATA,
            "BBREF_BOXSCORES": ScrapeCondition.ONLY_MISSING_DATA,
        }
    )
    rescrape_mlb_api: Dict[DataSet, bool] = field(
        default_factory={"BROOKS_GAMES_FOR_DATE": False, "BROOKS_PITCH_LOGS": False}
    )
    always_parse_mlb_api: Dict[DataSet, bool] = field(
        default_factory={"BROOKS_GAMES_FOR_DATE": False, "BROOKS_PITCH_LOGS": False}
    )
    combine_game_data: ScrapeCondition = ScrapeCondition.ONLY_MISSING_DATA
    backup_db: bool = False
    backup_combined_data_json: bool = False
    upload_backup_files_to_s3: bool = False
    restart_dokku_container: bool = False
