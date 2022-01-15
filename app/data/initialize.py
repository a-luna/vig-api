import os
from pathlib import Path

from app.data.download_manager import DownloadManager, RemoteFileInfo

MLB_SEASONS = [2017, 2018, 2019, 2020, 2021]
S3_BUCKET = "https://vig-api.us-southeast-1.linodeobjects.com"
SQLITE_DB = "vig.db"
DATA_FOLDER = Path(__file__).parent


def initialize():
    set_env_variables()
    db_file = RemoteFileInfo(f"{S3_BUCKET}/{SQLITE_DB}.zip", f"{S3_BUCKET}/{SQLITE_DB}.zip.md5", DATA_FOLDER)
    season_data_files = [get_season_data_file_info(year) for year in MLB_SEASONS]
    manager = DownloadManager([db_file, *season_data_files])
    manager.run()


def set_env_variables():
    os.environ["ENV"] = "PROD"
    os.environ["DOTENV_FILE"] = str(DATA_FOLDER.joinpath(".env"))
    os.environ["CONFIG_FILE"] = str(DATA_FOLDER.joinpath("vig.config.json"))
    os.environ["DATABASE_URL"] = f"sqlite:///{DATA_FOLDER.joinpath(SQLITE_DB)}"


def get_season_data_file_info(year):
    return RemoteFileInfo(
        f"{S3_BUCKET}/{year}.zip", f"{S3_BUCKET}/{year}.zip.md5", DATA_FOLDER.joinpath(f"json/{year}")
    )


if __name__ == "__main__":
    initialize()
