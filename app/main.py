from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi_redis_cache import FastApiRedisCache, cache
from starlette.responses import RedirectResponse
from vigorish.app import Vigorish

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    docs_url=None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=settings.REDIS_URL,
        response_header=settings.CACHE_HEADER,
        ignore_arg_types=[Vigorish],
    )


@app.get(f"{settings.API_VERSION}/docs", include_in_schema=False)
@cache()
async def swagger_ui_html():
    return get_swagger_ui_html(
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        openapi_url=app.openapi_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/", include_in_schema=False)
def get_api_root():
    api_docs_url = app.url_path_for("swagger_ui_html")
    return RedirectResponse(url=api_docs_url, status_code=int(HTTPStatus.PERMANENT_REDIRECT))


app.include_router(api_router, prefix=settings.API_VERSION)
