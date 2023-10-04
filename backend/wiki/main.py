import uvicorn
from fastapi import FastAPI

from wiki.api import api_router
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


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
