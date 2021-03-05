import os
from pathlib import Path
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings
from dotenv import load_dotenv

APP_ROOT = Path(__file__).parent.parent.parent
DOTENV_FILE = os.environ.get("DOTENV_FILE", str(APP_ROOT.joinpath(".env")))
load_dotenv(dotenv_path=DOTENV_FILE)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DOTENV_FILE: Path = Path(DOTENV_FILE)
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = "vig-api.aaronluna.dev"
    SERVER_HOST: Optional[AnyHttpUrl] = "http://vig-api.aaronluna.dev"
    PROJECT_NAME: Optional[str] = "Vigorish API - MLB Data"

    class Config:
        case_sensitive = True


settings = Settings()
