import json
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, RedisDsn

from app.data.initialize import download_and_extract_zip_files, set_env_variables


class Settings(BaseSettings):
    if str(Path(__file__).resolve()).startswith("/app"):
        download_and_extract_zip_files()
        set_env_variables()
    else:
        APP_ROOT = Path(__file__).parent.parent.parent.resolve()
        os.environ["DOTENV_FILE"] = str(APP_ROOT.joinpath(".env"))
        load_dotenv(dotenv_path=os.environ["DOTENV_FILE"])

    API_VERSION: str = os.environ.get("API_VERSION")
    DOTENV_FILE: Path = Path(os.environ.get("DOTENV_FILE"))
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = os.environ.get("SERVER_NAME")
    SERVER_HOST: Optional[AnyHttpUrl] = os.environ.get("SERVER_HOST")
    PROJECT_NAME: Optional[str] = os.environ.get("PROJECT_NAME")
    CORS_ALLOW_ORIGINS: List[str] = json.loads(os.environ.get("CORS_ALLOW_ORIGINS"))
    REDIS_URL: RedisDsn = os.environ.get("REDIS_URL")
    CACHE_HEADER: str = os.environ.get("CACHE_HEADER")

    class Config:
        case_sensitive = True


settings = Settings()
