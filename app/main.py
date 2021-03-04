from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")


@app.get("/")
def get_api_root():
    return {"message": "Welcome to Vigorish MLB Data API"}


app.include_router(api_router, prefix=settings.API_V1_STR)
