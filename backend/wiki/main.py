import logging

import uvicorn
import yaml
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from wiki.api import api_router
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiErrorResponse, HealthCheck
from wiki.config import settings
from wiki.database.deps import db_metadata_create_all
from wiki.wiki_logging import setup_logging
from wiki.wiki_logging.middleware import WikiRouterLoggerMiddleware

wiki_logger = logging.getLogger(__name__)


api = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=settings.API_SERVERS
)

add_pagination(api)

@api.exception_handler(WikiException)
async def wiki_exception_handler(request: Request, exc: WikiException):
    wiki_logger.info(msg=exc)
    return JSONResponse(
        status_code=exc.http_status_code,
        content=WikiErrorResponse(
            message=exc.message,
            error_code=WikiErrorCode(exc.error_code)
        ).model_dump()
    )


@api.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    wiki_logger.error(exc, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "INTERNAL_SERVER_ERROR",
            "error_code": WikiErrorCode.GENERIC_ERROR
        }
    )


if settings.BACKEND_CORS_ORIGINS:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


api.middleware("http")(
    WikiRouterLoggerMiddleware()
)


@api.get(f"{settings.API_V1_STR}/swagger.yaml", include_in_schema=False)
async def get_swagger():
    openapi_json = api.openapi()
    with open("./docs/swagger.yaml", "w") as file:
        yaml.dump(openapi_json, file)
    return openapi_json


@api.get(
    "/health",
    tags=["HealthCheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


if settings.DB_METADATA_CREATE_ALL:
    @api.on_event("startup")
    async def startup_event_db_metadata_create_all():
        await db_metadata_create_all()


@api.on_event("shutdown")
async def shutdown():
    wiki_logger.info("Shutdown server")


# frontend = FastAPI()
api.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    setup_logging()
    wiki_logger.info("Started server")
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="warning")
