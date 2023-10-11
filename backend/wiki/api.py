from fastapi import APIRouter
from starlette.responses import JSONResponse

from wiki.auth.routers import auth_router
from wiki.organization.router import organization_router
from wiki.user.router import user_router

api_router = APIRouter(
    default_response_class=JSONResponse
)

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(organization_router, prefix="/organization", tags=["Organization"])
