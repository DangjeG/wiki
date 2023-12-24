from fastapi import APIRouter
from starlette.responses import JSONResponse

from wiki.admins.router import admins_router
from wiki.auth.routers import auth_router
from wiki.permissions.object.router import object_permission_router
from wiki.permissions.domain.router import permission_domain_router
from wiki.wiki_api_client.api_client_router import wiki_api_client_router
from wiki.wiki_api_client.api_key_router import wiki_api_key_router
from wiki.user.router import user_router
from wiki.user_group.router import user_group_router
from wiki.wiki_workspace.block.router import block_router
from wiki.wiki_workspace.document.export.router import document_export_router
from wiki.wiki_workspace.document.router import document_router
from wiki.wiki_workspace.document_template.router import document_template_router
from wiki.wiki_workspace.router import workspace_router
from wiki.wiki_workspace.versioning.router import versioning_workspace_router
from wiki.assets_storage.router import asset_storage_router

api_router = APIRouter(
    default_response_class=JSONResponse
)

api_router.include_router(admins_router, prefix="/admins", tags=["Admins"])
api_router.include_router(permission_domain_router, prefix="/permission_domain", tags=["PermissionsDomain"])
api_router.include_router(object_permission_router, prefix="/permission_object", tags=["PermissionsObject"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(user_group_router, prefix="/user_group", tags=["UserGroup"])
api_router.include_router(wiki_api_key_router, prefix="/api_key", tags=["WikiApiClient"])
api_router.include_router(wiki_api_client_router, prefix="/api_client", tags=["WikiApiClient"])

api_router.include_router(workspace_router, prefix="/workspace", tags=["Workspace"])
api_router.include_router(document_router, prefix="/document", tags=["WorkspaceDocument"])
api_router.include_router(document_export_router, prefix="/document", tags=["ExportDocument"])
api_router.include_router(document_template_router, prefix="/document_template", tags=["DocumentTemplate"])
api_router.include_router(block_router, prefix="/blocks", tags=["WorkspaceBlocks"])
api_router.include_router(versioning_workspace_router, prefix="/versioning", tags=["WorkspaceVersioning"])
api_router.include_router(asset_storage_router, prefix="/asset_storage", tags=["AssetStorage"])
