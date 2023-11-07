from datetime import datetime
from uuid import UUID

from pydantic import constr

from wiki.models import WikiBase
from wiki.user.schemas import UserBaseInfoResponse


class VersionBlockInfo(WikiBase):
    commit_id: constr(min_length=64, max_length=64)
    object_id: UUID
    committer_user: UserBaseInfoResponse
    created_at: datetime


class VersionDocumentInfo(VersionBlockInfo):
    is_published: bool = False
