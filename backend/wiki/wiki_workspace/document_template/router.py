from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.database.deps import get_db
from wiki.wiki_workspace.document_template.model import DocumentTemplate
from wiki.wiki_workspace.document_template.repository import DocumentTemplateRepository
from wiki.wiki_workspace.document_template.schemas import DocumentTemplateInfoResponse, DocumentTemplateFilter, \
    CreateDocumentTemplate

document_template_router = APIRouter()

@document_template_router.get(
    "/all",
    response_model=Page[DocumentTemplateInfoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all document templates"
)
async def get_all_document_templates(
        document_template_filter: DocumentTemplateFilter = Depends(DocumentTemplateFilter),
        session: AsyncSession = Depends(get_db)
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
        session: AsyncSession = Depends(get_db)
):
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

    document_template = await document_template_repository.get_document_template_by_it(document_template_id)

    return DocumentTemplateInfoResponse(
        id=document_template.id,
        title=document_template.title,
        description=document_template.description,
        document_id=document_template.document_id,
        document_template_type=document_template.document_template_type,
        creator_user_id=document_template.creator_user_id
    )
