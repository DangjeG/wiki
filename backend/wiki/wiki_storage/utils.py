from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.document.repository import DocumentRepository


def forming_document_storage_path(unique_names_parents_documents: list[str],
                                  unique_block_name: str) -> str:
    if len(unique_names_parents_documents) < 1:
        raise ValueError
    path = f"{'/'.join(unique_names_parents_documents)}/{unique_block_name}.html"

    return path


async def get_unique_names_parents_documents(document: Document, document_repository: DocumentRepository) -> list[str]:
    unique_names_parents_documents = []
    while document.parent_document_id is not None:
        unique_names_parents_documents.append(str(document.id))
        document = await document_repository.get_document_by_id(document.parent_document_id)
    unique_names_parents_documents.reverse()

    return unique_names_parents_documents
