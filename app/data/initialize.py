import os
from pathlib import Path

from app.data.download_manager import DownloadManager, RemoteFileInfo

MLB_SEASONS = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
S3_BUCKET = "https://vig-api.us-southeast-1.linodeobjects.com"
SQLITE_DB = "vig.db"
DATA_FOLDER = Path(__file__).parent
DOTENV_FILE_DEFAULT = DATA_FOLDER.joinpath(".env")


def initialize():
    delete_dotenv_file()
    set_env_variables()
    create_dotenv_file()
    if os.environ.get("ENV") == "PROD":
        DownloadManager(get_remote_file_info()).run()


def delete_dotenv_file():
    dotenv_file = Path(os.environ.get("DOTENV_FILE", str(DOTENV_FILE_DEFAULT)))
    if dotenv_file.exists():
        dotenv_file.unlink()


def set_env_variables():
    os.environ["DOTENV_FILE"] = str(DOTENV_FILE_DEFAULT)
    if str(Path(__file__).resolve()).startswith("/code"):
        os.environ["ENV"] = "PROD"
        os.environ["CONFIG_FILE"] = str(DATA_FOLDER.joinpath("vig.config.json"))
        os.environ["DATABASE_URL"] = f"sqlite:///{DATA_FOLDER.joinpath(SQLITE_DB)}"
    else:
        os.environ["ENV"] = "DEV"
        os.environ["PROJECT_NAME"] = "Vigorish API - MLB Data"
        os.environ["API_VERSION"] = "/api/v1"
        os.environ["REDIS_URL"] = "redis://127.0.0.1:6379"
        os.environ["SERVER_NAME"] = "vig-api.aaronluna.dev"
        os.environ["SERVER_HOST"] = "https://vig-api.aaronluna.dev"
        os.environ["CACHE_HEADER"] = "X-Vigorish-Cache"
        os.environ["CONFIG_FILE"] = "/Users/aaronluna/Projects/custom_scripts/python/src/custom_scripts/mlb/scrape/vig.config.json"
        os.environ["DATABASE_URL"] = "sqlite:////Users/aaronluna/Projects/custom_scripts/python/src/custom_scripts/mlb/scrape/vig.db"


def create_dotenv_file():
    dotenv_dict = {"CONFIG_FILE": os.environ.get("CONFIG_FILE"), "DATABASE_URL": os.environ.get("DATABASE_URL")}
    env_var_strings = [f"{name}={value}" for name, value in dotenv_dict.items()]
    DOTENV_FILE_DEFAULT.write_text("\n".join(env_var_strings))


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
