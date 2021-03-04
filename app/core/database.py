from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from vigorish.app import Vigorish

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_vig_app(session: Session = Depends(get_db_session)):
    return Vigorish(dotenv_file=settings.DOTENV_FILE, db_engine=engine, db_session=session)
