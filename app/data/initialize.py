import os
from pathlib import Path
from zipfile import ZipFile

from app.data.util import download_file, get_file_name_from_url, validate_file

MLB_SEASONS = [2017, 2018, 2019, 2020, 2021]
S3_BUCKET = "https://alunapublic.s3.us-west-1.amazonaws.com/vig-api"
SQLITE_DB = "vig.db"

DATA_FOLDER = Path(__file__).parent
DOTENV_FILE = DATA_FOLDER.joinpath(".env")
CONFIG_FILE = DATA_FOLDER.joinpath("vig.config.json")
DATABASE_URL = f"sqlite:///{DATA_FOLDER.joinpath(SQLITE_DB)}"


def set_env_variables():
    os.environ["ENV"] = "PROD"
    os.environ["DOTENV_FILE"] = str(DOTENV_FILE)
    os.environ["CONFIG_FILE"] = str(CONFIG_FILE)
    os.environ["DATABASE_URL"] = DATABASE_URL


def download_files_from_s3():
    retry, error = download_files()
    if not error and not retry:
        print("All files were downloaded successfully.")
        return (retry, error)
    if retry:
        retry2, error2 = download_files(retry)
        error.extend(error2)
        retry = retry2
        if not error and not retry:
            print("All files were downloaded successfully.")
            return (retry, error)
    if error:
        plural = "files were" if len(error) > 1 else "file was"
        errors = "\n".join(f"{get_file_name_from_url(url)} error: {message}" for (url, message) in error)
        print(f"{len(error)} {plural} not downloaded successfully:\n{errors}")
    if retry:
        plural = "files" if len(retry) > 1 else "file"
        print(f"{len(retry)} {plural} partially downloaded after two attempts:\n{retry}")
    if retry or error:
        raise ValueError("Failed to download vig db and yearly data files!")


def download_files():
    retry, error = [], []
    for file_info in get_data_file_urls():
        url, hash_url, target_folder = file_info
        get_file_result = download_file(url, target_folder)
        get_hash_result = download_file(hash_url, target_folder)
        retry, error = verify_file_download(get_file_result, get_hash_result, file_info, retry, error)
    return (retry, error)


def get_data_file_urls():
    urls = [get_vig_database_urls()]
    urls.extend([get_combined_data_urls_for_season(year) for year in MLB_SEASONS])
    return urls


def get_vig_database_urls():
    return [
        f"{S3_BUCKET}/{SQLITE_DB}.zip",
        f"{S3_BUCKET}/{SQLITE_DB}.zip.md5",
        DATA_FOLDER,
    ]


def get_combined_data_urls_for_season(year):
    return [
        f"{S3_BUCKET}/{year}.zip",
        f"{S3_BUCKET}/{year}.zip.md5",
        DATA_FOLDER.joinpath(f"json/{year}"),
    ]


def verify_file_download(get_file_result, get_hash_result, file_info, retry, error):
    if get_file_result.success and get_hash_result.success:
        return (retry, error)
    if (
        "Received fewer bytes than expected" in get_file_result.error
        or "Received fewer bytes than expected" in get_hash_result.error
    ):
        retry.append(file_info)
    if get_file_result.failure and "Received fewer bytes than expected" not in get_file_result.error:
        error.append((file_info[0], get_file_result.error))
    if get_hash_result.failure and "Received fewer bytes than expected" not in get_hash_result.error:
        error.append((file_info[1], get_hash_result.error))
    return (retry, error)


def extract_zip_files():
    for zip_file_path, hash_file_path in get_data_file_paths():
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


def get_data_file_paths():
    data_files = [get_vig_database_filepaths()]
    data_files.extend([get_combined_data_filepaths_for_season(year) for year in MLB_SEASONS])
    return data_files


def get_vig_database_filepaths():
    return (DATA_FOLDER.joinpath(f"{SQLITE_DB}.zip"), DATA_FOLDER.joinpath(f"{SQLITE_DB}.zip.md5"))


def get_combined_data_filepaths_for_season(year):
    folderpath = DATA_FOLDER.joinpath(f"json/{year}")
    return (folderpath.joinpath(f"{year}.zip"), folderpath.joinpath(f"{year}.zip.md5"))
