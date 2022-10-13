import hashlib
import requests
from pathlib import Path
from urllib.parse import urlsplit

from tqdm import tqdm
from vigorish.util.result import Result

CHUNK_SIZE = 1024


def download_file(url: str, local_folder: Path, chunk_size: int = None):
    file_name = get_file_name_from_url(url)
    local_file_path = local_folder.joinpath(file_name)
    r = requests.head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    accept_ranges = r.headers.get("accept-ranges", 'none')
    if not remote_file_size:
        return Result.Fail(f'Request for "{file_name}" did not return a response containing the file size.')
    local_file_size = 0
    resume_header = None
    fopen_mode = "wb"
    if not local_file_path.exists():
        print(f'"{file_name}" does not exist. Downloading...')
    else:
        if accept_ranges == 'bytes':
            local_file_size = local_file_path.stat().st_size
            if local_file_size == remote_file_size:
                print(f'"{file_name}" is complete. Skipping...')
                return Result.Ok(local_file_path)
            resume_header = {"Range": f"bytes={local_file_size}-"}
            fopen_mode = "ab"
            print(f'"{file_name}" is incomplete. Resuming...')
        else:
            print(f'The web host for "{file_name}" does not support resuming partial downloads. Beginning new download...')
            local_file_path.unlink()
    
    if not chunk_size:
        chunk_size = CHUNK_SIZE
    r = requests.get(url, stream=True, headers=resume_header)
    with open(local_file_path, fopen_mode) as f:
        with tqdm(
            total=remote_file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=chunk_size,
            desc=local_file_path.name,
            initial=local_file_size,
            ascii=True,
            miniters=1,
        ) as pbar:
            for chunk in r.iter_content(32 * chunk_size):
                f.write(chunk)
                pbar.update(len(chunk))

    local_file_size = local_file_path.stat().st_size
    if local_file_size == remote_file_size:
        return Result.Ok(local_file_path)
    more_or_fewer = "more" if local_file_size > remote_file_size else "fewer"
    error = (
        f'Recieved {more_or_fewer} bytes than expected for "{file_name}"!\n'
        f"Expected File Size: {remote_file_size:,} bytes\n"
        f"Received File Size: {local_file_size:,} bytes"
    )
    return Result.Fail(error)


def get_file_name_from_url(url):
    return Path(urlsplit(url).path).name


def validate_file(local_file_path: Path, hash_file_path: Path, chunk_size: int = None) -> Result:
    if not local_file_path.exists():
        return Result.Fail(f"Unable to locate file: {local_file_path}")
    if not chunk_size:
        chunk_size = CHUNK_SIZE
    md5 = hashlib.md5()
    with open(local_file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return (
        Result.Ok()
        if md5.hexdigest() == hash_file_path.read_text()
        else Result.Fail(f"MD5 hash for {local_file_path.name} is incorrect!")
    )
