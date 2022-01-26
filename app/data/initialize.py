import os
from pathlib import Path

from app.data.download_manager import DownloadManager, RemoteFileInfo

MLB_SEASONS = [2017, 2018, 2019, 2020, 2021]
S3_BUCKET = "https://vig-api.us-southeast-1.linodeobjects.com"
SQLITE_DB = "vig.db"
DATA_FOLDER = Path(__file__).parent


def initialize():
    set_env_variables()
    remote_files = get_remote_file_info()
    manager = DownloadManager(remote_files)
    manager.run()


def set_env_variables():
    if str(Path(__file__).resolve()).startswith("/app"):
        os.environ["ENV"] = "PROD"
    elif str(Path(__file__).resolve()).startswith("/workspace"):
        os.environ["ENV"] = "DEV"
        os.environ["PROJECT_NAME"] = "Vigorish API - MLB Data"
        os.environ["API_VERSION"] = "/api/v1"
        os.environ["REDIS_URL"] = "redis://127.0.0.1:6379"
        os.environ["SERVER_NAME"] = "vig-api.aaronluna.dev"
        os.environ["SERVER_HOST"] = "https://vig-api.aaronluna.dev"
        os.environ["CACHE_HEADER"] = "X-Vigorish-Cache"
    os.environ["DOTENV_FILE"] = str(DATA_FOLDER.joinpath(".env"))
    os.environ["CONFIG_FILE"] = str(DATA_FOLDER.joinpath("vig.config.json"))
    os.environ["DATABASE_URL"] = f"sqlite:///{DATA_FOLDER.joinpath(SQLITE_DB)}"


def get_remote_file_info():
    remote_files = [
        RemoteFileInfo(
            f"{S3_BUCKET}/{SQLITE_DB}.zip",
            f"{S3_BUCKET}/{SQLITE_DB}.zip.md5",
            DATA_FOLDER,
        )
    ]
    for year in MLB_SEASONS:
        remote_files.append(
            RemoteFileInfo(
                f"{S3_BUCKET}/{year}.zip", f"{S3_BUCKET}/{year}.zip.md5", DATA_FOLDER.joinpath(f"json/{year}")
            )
        )
    return remote_files


if __name__ == "__main__":
    initialize()
