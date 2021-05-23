import os
from pathlib import Path
from zipfile import ZipFile

from app.data.util import download_file, get_file_name_from_url, validate_file

S3_BUCKET = "https://alunapublic.s3.us-west-1.amazonaws.com/vig-api"
SQLITE_DB = "vig.db"

DB_ZIP_FILE = f"{SQLITE_DB}.zip"
DB_ZIP_FILE_URL = f"{S3_BUCKET}/{DB_ZIP_FILE}"
DATA_FOLDER = Path(__file__).parent
DB_ZIP_FILE_PATH = DATA_FOLDER.joinpath(DB_ZIP_FILE)
DB_ZIP_FILE_HASH = f"{DB_ZIP_FILE}.md5"
DB_ZIP_FILE_HASH_URL = f"{S3_BUCKET}/{DB_ZIP_FILE_HASH}"
DB_ZIP_FILE_HASH_FILE_PATH = DATA_FOLDER.joinpath(DB_ZIP_FILE_HASH)

COMBINED_DATA_2017 = "2017.zip"
COMBINED_DATA_2017_URL = f"{S3_BUCKET}/{COMBINED_DATA_2017}"
COMBINED_DATA_2017_FOLDER = DATA_FOLDER.joinpath("json/2017")
COMBINED_DATA_2017_FILE_PATH = COMBINED_DATA_2017_FOLDER.joinpath(COMBINED_DATA_2017)
COMBINED_DATA_2017_HASH = f"{COMBINED_DATA_2017}.md5"
COMBINED_DATA_2017_HASH_URL = f"{S3_BUCKET}/{COMBINED_DATA_2017_HASH}"
COMBINED_DATA_2017_HASH_FILE_PATH = COMBINED_DATA_2017_FOLDER.joinpath(COMBINED_DATA_2017_HASH)

COMBINED_DATA_2018 = "2018.zip"
COMBINED_DATA_2018_URL = f"{S3_BUCKET}/{COMBINED_DATA_2018}"
COMBINED_DATA_2018_FOLDER = DATA_FOLDER.joinpath("json/2018")
COMBINED_DATA_2018_FILE_PATH = COMBINED_DATA_2018_FOLDER.joinpath(COMBINED_DATA_2018)
COMBINED_DATA_2018_HASH = f"{COMBINED_DATA_2018}.md5"
COMBINED_DATA_2018_HASH_URL = f"{S3_BUCKET}/{COMBINED_DATA_2018_HASH}"
COMBINED_DATA_2018_HASH_FILE_PATH = COMBINED_DATA_2018_FOLDER.joinpath(COMBINED_DATA_2018_HASH)

COMBINED_DATA_2019 = "2019.zip"
COMBINED_DATA_2019_URL = f"{S3_BUCKET}/{COMBINED_DATA_2019}"
COMBINED_DATA_2019_FOLDER = DATA_FOLDER.joinpath("json/2019")
COMBINED_DATA_2019_FILE_PATH = COMBINED_DATA_2019_FOLDER.joinpath(COMBINED_DATA_2019)
COMBINED_DATA_2019_HASH = f"{COMBINED_DATA_2019}.md5"
COMBINED_DATA_2019_HASH_URL = f"{S3_BUCKET}/{COMBINED_DATA_2019_HASH}"
COMBINED_DATA_2019_HASH_FILE_PATH = COMBINED_DATA_2019_FOLDER.joinpath(COMBINED_DATA_2019_HASH)

DATA_FILES = [
    {"url": DB_ZIP_FILE_URL, "hash_url": DB_ZIP_FILE_HASH_URL, "folder": DATA_FOLDER},
    {"url": COMBINED_DATA_2017_URL, "hash_url": COMBINED_DATA_2017_HASH_URL, "folder": COMBINED_DATA_2017_FOLDER},
    {"url": COMBINED_DATA_2018_URL, "hash_url": COMBINED_DATA_2018_HASH_URL, "folder": COMBINED_DATA_2018_FOLDER},
    {"url": COMBINED_DATA_2019_URL, "hash_url": COMBINED_DATA_2019_HASH_URL, "folder": COMBINED_DATA_2019_FOLDER},
]

ZIP_FILES = [
    (DB_ZIP_FILE_PATH, DB_ZIP_FILE_HASH_FILE_PATH),
    (COMBINED_DATA_2017_FILE_PATH, COMBINED_DATA_2017_HASH_FILE_PATH),
    (COMBINED_DATA_2018_FILE_PATH, COMBINED_DATA_2018_HASH_FILE_PATH),
    (COMBINED_DATA_2019_FILE_PATH, COMBINED_DATA_2019_HASH_FILE_PATH),
]

DOTENV_FILE = DATA_FOLDER.joinpath(".env")
CONFIG_FILE = DATA_FOLDER.joinpath("vig.config.json")
DATABASE_URL = f"sqlite:///{DATA_FOLDER.joinpath(SQLITE_DB)}"


def download_and_extract_zip_files():
    (error, retry) = download_files_from_s3()
    if error or retry:
        raise ValueError("Failed to download vig db and yearly data files!")
    for zip_file_path, hash_file_path in ZIP_FILES:
        print(f"Calculating MD5 hash for: {zip_file_path.name}...")
        result = validate_file(zip_file_path, hash_file_path)
        if result.failure:
            raise ValueError(result.error)
        print(f"MD5 hash for {zip_file_path.name} successfully validated")
        print(f"Extracting contents of zip file: {zip_file_path.name}...")
        with ZipFile(zip_file_path, mode="r") as zip:
            zip.extractall(path=zip_file_path.parent)
        zip_file_path.unlink()
        hash_file_path.unlink()
        print(f"Deleted {zip_file_path.name} after all contents were extracted.")


def download_files_from_s3():
    retry, error = download_files(DATA_FILES)
    if not error and not retry:
        print("All files were downloaded successfully.")
        return (error, retry)
    if retry:
        retry2, error2 = download_files(retry)
        error.extend(error2)
        retry = retry2
        if not error and not retry:
            print("All files were downloaded successfully.")
            return (error, retry)
    if error:
        plural = "files were" if len(error) > 1 else "file was"
        files = "\n".join(get_file_name_from_url(url) for url in error)
        print(f"{len(error)} {plural} not downloaded successfully:\n{files}")
    if retry:
        plural = "files" if len(retry) > 1 else "file"
        files = "\n".join(get_file_name_from_url(url) for url in retry)
        print(f"{len(retry)} {plural} partially downloaded after two attempts:\n{files}")
    return (error, retry)


def download_files(file_list):
    retry, error = [], []
    for file_dict in file_list:
        get_file_result = download_file(file_dict["url"], file_dict["folder"])
        get_hash_result = download_file(file_dict["hash_url"], file_dict["folder"])

        if get_file_result.failure:
            print(get_file_result.error)
        if get_hash_result.failure:
            print(get_hash_result.error)
        if get_file_result.success and get_hash_result.success:
            continue

        if "Received fewer bytes than expected" in get_file_result.error:
            retry.append(file_dict)
        else:
            error.append(file_dict["url"])
        if "Received fewer bytes than expected" in get_hash_result.error:
            retry.append(file_dict)
        else:
            error.append(file_dict["hash_url"])

    return (retry, error)


def set_env_variables():
    os.environ["DOTENV_FILE"] = str(DOTENV_FILE)
    os.environ["CONFIG_FILE"] = str(CONFIG_FILE)
    os.environ["DATABASE_URL"] = DATABASE_URL
