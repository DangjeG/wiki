from uuid import UUID

from sqlalchemy import select, and_

from wiki.database.repository import BaseRepository
from wiki.wiki_workspace.document_template.model import DocumentTemplate
from wiki.wiki_workspace.document_template.schemas import CreateDocumentTemplate, DocumentTemplateFilter


class DocumentTemplateRepository(BaseRepository):
    async def create_document_template(self, document_template: CreateDocumentTemplate):
        new_template: DocumentTemplate = DocumentTemplate(
            title=document_template.title,
            description=document_template.description,
            document_id=document_template.document_id,
            orig_commit_id=document_template.orig_commit_id,
            creator_user_id=document_template.creator_user_id,
            document_template_type=document_template.document_template_type,
        )
        self.session.add(new_template)

        return new_template

    async def get_all_document_templates_filter(self, document_template_filter: DocumentTemplateFilter) -> list[DocumentTemplate]:
        filters = []
        if document_template_filter.title is not None:
            filters.append(DocumentTemplate.title.ilike(f'%{document_template_filter.title}%'))
        if document_template_filter.description is not None:
            filters.append(DocumentTemplate.description.ilike(f'%{document_template_filter.description}%'))
        if document_template_filter.document_template_type is not None:
            filters.append(DocumentTemplate.document_template_type.like(str(document_template_filter.document_template_type)))
        if document_template_filter.creator_user_id is None:
            filters.append(DocumentTemplate.is_default_template.like(True))

        result = self.session.execute(select(DocumentTemplate).where(and_(*filters)))

        return result.scalars().all()

    async def get_document_template_by_id(self, document_template_id: UUID):
        document_template = self.session.get(DocumentTemplate, document_template_id)

        return document_template
