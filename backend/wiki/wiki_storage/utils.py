from functools import wraps
from typing import Optional
from uuid import UUID

from lakefs_client import ApiException
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


def menage_lakefs_api_exception_method(e: Optional[WikiException] = None):
    def decorator(f):
        @wraps(f)
        def wrapped_f(self, *args, **kwargs):
            try:
                result = f(self, *args, **kwargs)
            except ApiException as exc:
                if e is not None:
                    raise e
                else:
                    raise WikiException(
                        message=exc.body,
                        error_code=WikiErrorCode.LAKEFS_API_EXCEPTION,
                        http_status_code=status.HTTP_400_BAD_REQUEST
                    )

            return result

        return wrapped_f

    return decorator
