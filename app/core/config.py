import os
from pathlib import Path
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings
from dotenv import load_dotenv

APP_ROOT = Path(__file__).parent.parent.parent
DOTENV_FILE = APP_ROOT.joinpath(".env")
os.environ["DOTENV_FILE"] = str(DOTENV_FILE)
load_dotenv(dotenv_path=DOTENV_FILE)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    DOTENV_FILE: Path = Path(os.environ.get("DOTENV_FILE"))
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = "vig.aaronluna.dev"
    SERVER_HOST: Optional[AnyHttpUrl] = "http://vig.aaronluna.dev"
    PROJECT_NAME: Optional[str] = "Vigorish API - MLB Data"

    class Config:
        case_sensitive = True


settings = Settings()
