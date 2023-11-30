from sqlalchemy import Column, ForeignKey, UniqueConstraint

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin
from wiki.permissions.object.schemas import IndividualObjectPermissionInfo


class IndividualObjectPermissionMixin(BaseObjectPermissionMixin):
    user_id = Column(ForeignKey("user.id"), nullable=False)

    # For each object there can be only one permission for each user
    __table_args__ = tuple(
        UniqueConstraint(
            "object_id",
            "user_id",
            name="individual_object_permission_uc")
    )

    def get_permission_info(self) -> IndividualObjectPermissionInfo:
        return IndividualObjectPermissionInfo(
            id=self.id,
            mode=self.mode,
            object=self.object_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user=self.user_id
        )


class IndividualWorkspacePermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False)


class IndividualDocumentPermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False)


class IndividualBlockPermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False)
