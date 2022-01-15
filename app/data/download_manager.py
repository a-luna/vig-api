from dataclasses import dataclass, field
from pathlib import Path
from zipfile import ZipFile

from app.data.util import download_file, get_file_name_from_url, validate_file

MAX_DOWNLOAD_ATTEMPTS = 5
PARTIAL_FILE_ERROR = "Received fewer bytes than expected"


@dataclass(frozen=True)
class RemoteFileInfo:
    url: str
    hash_url: str
    target_folder: Path

    @property
    def zip_filename(self):
        return get_file_name_from_url(self.url)

    @property
    def hash_filename(self):
        return get_file_name_from_url(self.hash_url)

    @property
    def zip_filepath(self):
        return self.target_folder.joinpath(self.zip_filename)

    @property
    def hash_filepath(self):
        return self.target_folder.joinpath(self.hash_filename)

    def verify_file_hash(self):
        return validate_file(self.zip_filepath, self.hash_filepath)


@dataclass
class DownloadFileTask:
    file_info: RemoteFileInfo
    attempts: int = 0
    success: bool = field(init=False)
    error: bool = field(init=False)
    unzipped: bool = field(init=False)
    message: str = field(init=False)

    def __post_init__(self):
        self.success = False
        self.error = False
        self.unzipped = False
        self.message = ""

    @property
    def zip_file(self):
        return self.file_info.zip_filename

    @property
    def filepath(self):
        return self.file_info.zip_filepath

    @property
    def attempts_remaining(self):
        return MAX_DOWNLOAD_ATTEMPTS - self.attempts

    def validate_file(self):
        print(f"Calculating MD5 hash for: {self.zip_file}...")
        result = self.file_info.verify_file_hash()
        if result.success:
            print(f"MD5 hash for {self.zip_file} successfully validated")
        else:
            print(result.error)
        return result

    def remove_files(self):
        self.file_info.zip_filepath.unlink()
        self.file_info.hash_filepath.unlink()


class DownloadManager:
    def __init__(self, files):
        self.tasks = [DownloadFileTask(file) for file in files]

    @property
    def remaining_tasks(self):
        return [task for task in self.tasks if not task.error and not task.success and task.attempts_remaining]

    @property
    def successful_tasks(self):
        return [task for task in self.tasks if task.success]

    @property
    def error_tasks(self):
        return [task for task in self.tasks if task.error]

    @property
    def ready_to_unzip_tasks(self):
        return [task for task in self.tasks if task.success and not task.unzipped]

    @property
    def all_tasks_successfully_complete(self):
        return all(task.success for task in self.tasks)

    @property
    def errors(self):
        errors = "\n".join(f"{task.zip_file}: {task.message}" for task in self.tasks if task.error)
        plural = "files were" if len(errors) > 1 else "file was"
        return f"{len(errors)} {plural} not downloaded successfully:\n{errors}"

    def run(self):
        while self.remaining_tasks:
            for task in self.remaining_tasks:
                self.download_files(task)
        if self.all_tasks_successfully_complete:
            self.extract_zip_files()
        self.show_results()

    def download_files(self, task):
        get_file_result = download_file(task.file_info.url, task.file_info.target_folder)
        get_hash_result = download_file(task.file_info.hash_url, task.file_info.target_folder)
        if get_file_result.success and get_hash_result.success:
            result = task.validate_file()
            if result.success:
                task.success = True
            else:
                task.error = True
                task.message = result.error
        elif any(PARTIAL_FILE_ERROR in e for e in [get_file_result.error, get_hash_result.error]):
            task.attempts += 1
            if not task.attempts_remaining:
                task.error = True
                task.message = f"Failed to download complete file after {MAX_DOWNLOAD_ATTEMPTS} attempts"
        else:
            task.error = True
            task.message = get_error_messages(get_file_result, get_hash_result, task)

    def extract_zip_files(self):
        for task in self.ready_to_unzip_tasks:
            print(f"Extracting contents of zip file: {task.zip_file}...")
            with ZipFile(task.filepath, mode="r") as zip:
                zip.extractall(path=task.filepath.parent)
            task.unzipped = True
            task.remove_files()
            print(f"Deleted {task.zip_file} after all contents were extracted.")

    def show_results(self):
        print("\n#### DOWNLOAD RESULTS ####")
        print(f"Success....: {len(self.successful_tasks)}")
        print(f"Error......: {len(self.error_tasks)}")
        print(f"Remaining..: {len(self.remaining_tasks)}\n")
        if self.error_tasks:
            print(self.errors)
        if self.all_tasks_successfully_complete:
            print("All files were downloaded successfully.")
        return


def get_error_messages(get_file_result, get_hash_result, task):
    error_messages = []
    if get_file_result.failure:
        error_messages.append(f"{get_file_result.error} ({task.zip_filename})")
    if get_hash_result.failure:
        error_messages.append(f"{get_hash_result.error} ({task.hash_filename})")
    return "\n".join(error_messages)
