import os
from pathlib import Path
from zipfile import ZipFile

DATA_FOLDER = Path(__file__).parent
DOTENV_FILE = DATA_FOLDER.joinpath(".env")
CONFIG_FILE = DATA_FOLDER.joinpath("vig.config.json")
DATABASE_URL = f"sqlite:///{DATA_FOLDER.joinpath('vig.db')}"
ZIP_FILES = [
    DATA_FOLDER.joinpath("vig.db.zip"),
    DATA_FOLDER.joinpath("json/2017/2017.zip"),
    DATA_FOLDER.joinpath("json/2018/2018.zip"),
    DATA_FOLDER.joinpath("json/2019/2019.zip"),
]


def extract_zip_files():
    for zip_file in ZIP_FILES:
        with ZipFile(zip_file, mode="r") as zip:
            zip.extractall(path=zip_file.parent)
        zip_file.unlink()


def set_env_variables():
    os.environ["DOTENV_FILE"] = str(DOTENV_FILE)
    os.environ["CONFIG_FILE"] = str(CONFIG_FILE)
    os.environ["DATABASE_URL"] = DATABASE_URL
