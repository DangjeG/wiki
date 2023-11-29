from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Uuid, ForeignKey, String, event, DateTime
from uuid_extensions import uuid7

from wiki.common.models import EnabledDeletedMixin
from wiki.database.core import Base
from wiki.database.utils import utcnow
from wiki.permissions.object.general.models import GeneralObjectPermissionMixin, GeneralDocumentPermission
from wiki.permissions.object.group.models import GroupObjectPermissionMixin, GroupDocumentPermission
from wiki.permissions.object.individual.models import IndividualObjectPermissionMixin, IndividualDocumentPermission
from wiki.permissions.object.interfaces import IGenObjectPermission
from wiki.permissions.object.schemas import (
    CreateGeneralObjectPermission,
    CreateGroupObjectPermission,
    CreateIndividualObjectPermission
)


class Document(Base, EnabledDeletedMixin, IGenObjectPermission):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    creator_user_id = Column(ForeignKey("user.id"), nullable=False)
    workspace_id = Column(ForeignKey("workspace.id"), nullable=False)
    parent_document_id = Column(ForeignKey("document.id"), nullable=True)

    current_published_version_commit_id = Column(String(64), nullable=True)
    last_published_version_at = Column(DateTime(timezone=True), nullable=False, default=utcnow())
    last_published_version_at._creation_order = 9998

    @staticmethod
    def _last_published_version_at(target, value, oldvalue, initiator):
        target.last_published_version_at = utcnow()

    @classmethod
    def __declare_last__(cls):
        super().__declare_last__()
        event.listen(cls.current_published_version_commit_id, "set", cls._last_published_version_at)

    def __init__(self,
                 title: str,
                 workspace_id: UUID,
                 creator_user_id: UUID,
                 parent_document_id: Optional[UUID] = None,
                 current_published_version_commit_id: Optional[str] = None):
        self.title = title
        self.workspace_id = workspace_id
        self.creator_user_id = creator_user_id
        self.parent_document_id = parent_document_id
        self.current_published_version_commit_id = current_published_version_commit_id

    def gen_general_object_permission(self, create_permission: CreateGeneralObjectPermission) -> GeneralObjectPermissionMixin:
        return GeneralDocumentPermission(
            mode=str(create_permission.mode),
            required_responsibility=str(create_permission.required_responsibility),
            object_id=self.id
        )

    def gen_group_object_permission(self, create_permission: CreateGroupObjectPermission) -> GroupObjectPermissionMixin:
        return GroupDocumentPermission(
            mode=str(create_permission.mode),
            group_id=create_permission.group_id,
            object_id=self.id
        )

    def gen_individual_object_permission(self, create_permission: CreateIndividualObjectPermission) -> IndividualObjectPermissionMixin:
        return IndividualDocumentPermission(
            mode=str(create_permission.mode),
            user_id=create_permission.user_id,
            object_id=self.id
        )
