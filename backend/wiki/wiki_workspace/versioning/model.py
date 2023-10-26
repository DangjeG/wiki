from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Uuid, String, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import TimeStampMixin
from wiki.database.core import Base


class VersionWorkspace(Base, TimeStampMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    parent_version_id = Column(ForeignKey("version_workspace.id"), nullable=True)
    commit_id = Column(String(64), unique=True, nullable=False)
    workspace_id = Column(ForeignKey("workspace.id"), nullable=False)
    committer_user_id = Column(ForeignKey("user.id"), nullable=False)
    branch = Column(String, nullable=False)

    def __init__(self,
                 commit_id: str,
                 workspace_id: UUID,
                 committer_user_id: UUID,
                 branch: str,
                 parent_version_id: Optional[UUID] = None):
        self.commit_id = commit_id
        self.workspace_id = workspace_id
        self.committer_user_id = committer_user_id
        self.branch = branch
        self.parent_version_id = parent_version_id
