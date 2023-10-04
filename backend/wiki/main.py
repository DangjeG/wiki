import uvicorn
import yaml
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.responses import JSONResponse

from wiki.api import api_router
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiErrorResponse
from wiki.config import settings


api = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# frontend = FastAPI()

api.include_router(api_router)

@api.get(f"/swagger.yaml", include_in_schema=False)
async def get_swagger():
    openapi_schema = get_openapi(title=f"{settings.PROJECT_NAME} API", version=settings.VERSION, routes=api.routes)
    with open("./docs/swagger.yaml", "w") as file:
        yaml.dump(openapi_schema, file)
    return openapi_schema


@api.exception_handler(WikiException)
async def cas_exception_handler(request: Request, exc: WikiException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content=WikiErrorResponse(
            message=exc.message,
            error_code=WikiErrorCode(exc.error_code)
        ).model_dump()
    )


@api.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, ex: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "INTERNAL_SERVER_ERROR",
            "error_code": WikiErrorCode.GENERIC_ERROR
        }
    )


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
