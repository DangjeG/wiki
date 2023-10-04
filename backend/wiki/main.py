import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

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


@api.get(f"/swagger.yaml", include_in_schema=False)
async def get_swagger():
    openapi_schema = get_openapi(title=f"{settings.PROJECT_NAME} API", version=settings.VERSION, routes=api.routes)
    with open("./docs/swagger.yaml", "w") as file:
        yaml.dump(openapi_schema, file)
    return openapi_schema


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
