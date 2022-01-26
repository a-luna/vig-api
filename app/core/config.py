import os
from pathlib import Path
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, RedisDsn

from app.data.initialize import initialize


class Settings(BaseSettings):
    initialize()

    ENV: str = os.environ.get("ENV")
    API_VERSION: str = os.environ.get("API_VERSION")
    DOTENV_FILE: Path = Path(os.environ.get("DOTENV_FILE"))
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = os.environ.get("SERVER_NAME")
    SERVER_HOST: Optional[AnyHttpUrl] = os.environ.get("SERVER_HOST")
    PROJECT_NAME: Optional[str] = os.environ.get("PROJECT_NAME")
    REDIS_URL: RedisDsn = os.environ.get("REDIS_URL")
    CACHE_HEADER: str = os.environ.get("CACHE_HEADER")

    class Config:
        case_sensitive = True


settings = Settings()
