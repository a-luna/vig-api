import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, RedisDsn

from app.data.initialize import extract_zip_files, set_env_variables


class Settings(BaseSettings):
    if str(Path(__file__).resolve()).startswith("/app"):
        extract_zip_files()
        set_env_variables()
    else:
        APP_ROOT = Path(__file__).parent.parent.parent.resolve()
        os.environ["DOTENV_FILE"] = str(APP_ROOT.joinpath(".env"))
        load_dotenv(dotenv_path=os.environ["DOTENV_FILE"])

    API_VERSION: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    DOTENV_FILE: Path = Path(os.environ.get("DOTENV_FILE"))
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = "vig-api.aaronluna.dev"
    SERVER_HOST: Optional[AnyHttpUrl] = "https://vig-api.aaronluna.dev"
    PROJECT_NAME: Optional[str] = "Vigorish API - MLB Data"
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:3000"]
    REDIS_URL: RedisDsn = os.environ.get("REDIS_URL")
    CACHE_HEADER: str = "X-Vigorish-Cache"

    class Config:
        case_sensitive = True


settings = Settings()
