from fastapi import APIRouter, Depends

from wiki.common.schemas import WikiUserHandlerData
from wiki.permissions.base import BasePermission
from wiki.wiki_api_client.enums import ResponsibilityType

wiki_api_client_router = APIRouter()


# @wiki_api_client_router.get(
#     ""
# )
# async def get_wiki_api_keys(
#         user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
# ):
#

