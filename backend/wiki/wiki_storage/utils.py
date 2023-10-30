from uuid import UUID

from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings


def forming_document_block_storage_path(document_ids: list[UUID],
                                        block_id: UUID) -> str:
    if len(document_ids) < 1:
        raise WikiException(
            message="The block must necessarily be attached to the document.",
            error_code=WikiErrorCode.GENERIC_ERROR,
            http_status_code=status.HTTP_400_BAD_REQUEST
        )
    path = f"{'/'.join([str(item) for item in document_ids])}/{str(block_id)}{settings.LAKEFS_DOCUMENT_BLOCK_FILE_EXT}"

    return path


def forming_document_storage_path(document_ids: list[UUID]):
    if len(document_ids) < 1:
        raise WikiException(
            message="At least one top-level document id must be specified to retrieve a document.",
            error_code=WikiErrorCode.GENERIC_ERROR,
            http_status_code=status.HTTP_400_BAD_REQUEST
        )
    path = f"{'/'.join([str(item) for item in document_ids])}"

    return path
