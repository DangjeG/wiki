from fastapi import APIRouter
from starlette.responses import JSONResponse

from wiki.auth.routers import auth_router
from wiki.wiki_api_client.api_client_router import wiki_api_client_router
from wiki.wiki_api_client.api_key_router import wiki_api_key_router
from wiki.organization.router import organization_router
from wiki.user.router import user_router

api_router = APIRouter(
    default_response_class=JSONResponse
)

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(organization_router, prefix="/organization", tags=["Organization"])
api_router.include_router(wiki_api_key_router, prefix="/api_key", tags=["WikiApiClient"])
api_router.include_router(wiki_api_client_router, prefix="/api_client", tags=["WikiApiClient"])
