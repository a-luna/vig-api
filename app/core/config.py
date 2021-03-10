import os
from pathlib import Path
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings
from dotenv import load_dotenv

from app.data.initialize import extract_zip_files, set_env_variables


class Settings(BaseSettings):
    if str(Path(__file__).resolve()).startswith("/app"):
        extract_zip_files()
        set_env_variables()
    else:
        APP_ROOT = Path(__file__).parent.parent.parent.resolve()
        os.environ["DOTENV_FILE"] = str(APP_ROOT.joinpath(".env"))
        load_dotenv(dotenv_path=os.environ["DOTENV_FILE"])

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    DOTENV_FILE: Path = Path(os.environ.get("DOTENV_FILE"))
    CONFIG_FILE: Path = Path(os.environ.get("CONFIG_FILE"))
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SERVER_NAME: Optional[str] = "vig-api.aaronluna.dev"
    SERVER_HOST: Optional[AnyHttpUrl] = "https://vig-api.aaronluna.dev"
    PROJECT_NAME: Optional[str] = "Vigorish API - MLB Data"

    class Config:
        case_sensitive = True


settings = Settings()
