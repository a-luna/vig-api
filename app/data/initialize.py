import os
from pathlib import Path
from zipfile import ZipFile

DATA_FOLDER = Path(__file__).parent

ZIP_FILES = [
    (DATA_FOLDER.joinpath("vig.db.zip"), DATA_FOLDER),
    (DATA_FOLDER.joinpath("json/2017/2017.zip"), DATA_FOLDER.joinpath("json/2017")),
    (DATA_FOLDER.joinpath("json/2018/2018.zip"), DATA_FOLDER.joinpath("json/2018")),
    (DATA_FOLDER.joinpath("json/2019/2019.zip"), DATA_FOLDER.joinpath("json/2019")),
]


def extract_zip_files():
    for (zip_file, extract_path) in ZIP_FILES:
        with ZipFile(zip_file, mode="r") as zip:
            zip.extractall(path=extract_path)
        zip_file.unlink()


def set_env_variables():
    os.environ["DOTENV_FILE"] = str(DATA_FOLDER.joinpath(".env"))
    os.environ["CONFIG_FILE"] = str(DATA_FOLDER.joinpath("vig.config.json"))
    os.environ["DATABASE_URL"] = f"sqlite:///{DATA_FOLDER.joinpath('vig.db')}"
