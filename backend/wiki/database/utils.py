from datetime import datetime, timezone
from enum import IntEnum
from functools import wraps
from typing import Optional

from sqlalchemy.exc import DatabaseError
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode


DELETED_USER_EMAIL_HOST = "example.com"
DELETED_USER_ID_PREFIX = "deleted_"
DELETED_USER_FIRST_NAME = "Deleted first name"
DELETED_USER_LAST_NAME = "Deleted last name"
DELETED_USER_SECOND_NAME = "Deleted second name"


class CommitMode(IntEnum):
    """
    Commit modes for the managed db methods
    """

    NONE = 0
    FLUSH = 1
    COMMIT = 2
    ROLLBACK = 3


def menage_db_commit_method(auto_commit: CommitMode = CommitMode.FLUSH):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match auto_commit:
                case CommitMode.FLUSH:
                    await self.session.flush()
                case CommitMode.COMMIT:
                    await self.session.commit()
                case CommitMode.ROLLBACK:
                    await self.session.rollback()

            return result

        return wrapped_f

    return decorator


class NotFoundResultMode(IntEnum):
    """
    Modes for resolving an empty query result from the database
    """

    NONE = 0
    EXCEPTION = 1


def manage_db_exception_method(ex: type[DatabaseError], raise_ex: Optional[WikiException] = None):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            try:
                return await f(self, *args, **kwargs)
            except ex:
                if raise_ex is not None:
                    raise raise_ex
        return wrapped_f
    return decorator


def menage_db_not_found_result_method(
        mode: NotFoundResultMode = NotFoundResultMode.EXCEPTION,
        ex: Optional[WikiException] = None
):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match mode:
                case NotFoundResultMode.NONE:
                    return result
                case NotFoundResultMode.EXCEPTION:
                    if result is None:
                        if ex is None:
                            raise WikiException(
                                message="Object not found",
                                error_code=WikiErrorCode.OBJECT_NOT_FOUND,
                                http_status_code=status.HTTP_404_NOT_FOUND
                            )
                        else:
                            raise ex
                    else:
                        return result

        return wrapped_f

    return decorator


def utcnow() -> datetime:
    """Return the current utc date and time with tzinfo set to UTC."""
    return datetime.now(timezone.utc)


def unaware_to_utc(d: datetime | None) -> datetime:
    """Set timezeno to UTC if datetime is unaware (tzinfo == None)."""
    if d and d.tzinfo is None:
        return d.replace(tzinfo=timezone.utc)
    return d
