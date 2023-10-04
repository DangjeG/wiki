from fastapi import APIRouter
from starlette.responses import JSONResponse

from wiki.auth.routers import auth_router

api_router = APIRouter(
    default_response_class=JSONResponse
)

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
