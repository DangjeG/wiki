from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import WikiUserHandlerData
from wiki.database.deps import get_db
from wiki.permissions.base import BasePermission
from wiki.permissions.object.enums import ObjectPermissionMode
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_workspace.document.repository import DocumentRepository
from wiki.wiki_workspace.document_template.model import DocumentTemplate
from wiki.wiki_workspace.document_template.repository import DocumentTemplateRepository
from wiki.wiki_workspace.document_template.schemas import (
    DocumentTemplateInfoResponse,
    DocumentTemplateFilter,
    CreateDocumentTemplate
)

document_template_router = APIRouter()


@document_template_router.get(
    "/all",
    response_model=Page[DocumentTemplateInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all document templates"
)
async def get_all_document_templates(
        document_template_filter: DocumentTemplateFilter = Depends(DocumentTemplateFilter),
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_template_repository: DocumentTemplateRepository = DocumentTemplateRepository(session)
    templates: list[DocumentTemplate] = await document_template_repository.get_all_document_templates_filter(document_template_filter)
    result_templates: list[DocumentTemplateInfoResponse] = []

    for template in templates:
        result_templates.append(DocumentTemplateInfoResponse(
            id=template.id,
            title=template.title,
            description=template.description,
            document_id=template.document_id,
            document_template_type=template.document_template_type,
            creator_user_id=template.creator_user_id
        ))

    return paginate(result_templates)


@document_template_router.post(
    "/",
    response_model=DocumentTemplateInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Add template"
)
async def create_document_template(
        document_template: CreateDocumentTemplate = Depends(CreateDocumentTemplate),
        session: AsyncSession = Depends(get_db),
        user: WikiUserHandlerData = Depends(BasePermission(responsibility=ResponsibilityType.VIEWER))
):
    document_repository = DocumentRepository(session)
    document = await document_repository.get_document_with_permission_by_id(user.id, document_template.document_id)
    if (user.wiki_api_client.responsibility == ResponsibilityType.ADMIN or
            ObjectPermissionMode(document.permission_mode) >= ObjectPermissionMode.ABILITY_USE_TEMPLATE):
        document_template_repository: DocumentTemplateRepository = DocumentTemplateRepository(session)

        new_document_template = await document_template_repository.create_document_template(document_template)

        return DocumentTemplateInfoResponse(
            id=new_document_template.id,
            title=new_document_template.title,
            description=new_document_template.description,
            document_id=new_document_template.document_id,
            document_template_type=new_document_template.document_template_type,
            creator_user_id=new_document_template.creator_user_id
        )
    else:
        raise WikiException(
            message="You can't create a template of them for this document. You must have permission to create templates for the document.",
            error_code=WikiErrorCode.DOCUMENT_CREATE_TEMPLATE_FORBIDDEN,
            http_status_code=status.HTTP_403_FORBIDDEN
        )


@document_template_router.get(
    "/",
    response_model=DocumentTemplateInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Add document template"
)
async def get_document_template_by_id(
        document_template_id: UUID,
        session: AsyncSession = Depends(get_db)
):
    document_template_repository: DocumentTemplateRepository = DocumentTemplateRepository(session)

    document_template = await document_template_repository.get_document_template_by_id(document_template_id)

    return DocumentTemplateInfoResponse(
        id=document_template.id,
        title=document_template.title,
        description=document_template.description,
        document_id=document_template.document_id,
        document_template_type=document_template.document_template_type,
        creator_user_id=document_template.creator_user_id
    )
