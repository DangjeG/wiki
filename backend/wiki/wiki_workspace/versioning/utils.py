from datetime import datetime
from functools import wraps
from uuid import UUID

from lakefs_client import ApiException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.user.utils import get_user_info
from wiki.wiki_workspace.versioning.schemas import VersionObjectInfo


async def get_version_object_info_list(results: dict, object_id: UUID, session: AsyncSession) -> list[VersionObjectInfo]:
    """
    :param results: Result get from the dictionary from lakefs answer
    :param object_id: Versioning object identifier (Document, block, etc.)
    :param session: Database session
    """

    return [VersionObjectInfo(
        commit_id=item.get("id"),
        object_id=object_id,
        committer_user=await get_user_info(UUID(item.get("metadata").get("committer_user_id")), session, is_full=False),
        created_at=datetime.fromtimestamp(int(item.get("creation_date")))
    ) for item in results]


def menage_lakefs_api_exception_method():
    def decorator(f):
        @wraps(f)
        def wrapped_f(self, *args, **kwargs):
            try:
                result = f(self, *args, **kwargs)
            except ApiException as e:
                raise WikiException(
                    message=e.body,
                    error_code=WikiErrorCode.LAKEFS_API_EXCEPTION,
                    http_status_code=status.HTTP_400_BAD_REQUEST
                )

            return result

        return wrapped_f

    return decorator
