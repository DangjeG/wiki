from sqlalchemy import Column, ForeignKey, Boolean

from wiki.database.core import Base
from wiki.permissions.object.base import BaseObjectPermissionMixin


class IndividualObjectPermissionMixin(BaseObjectPermissionMixin):
    is_able_delegate_access = Column(Boolean, nullable=False, default=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)


class IndividualWorkspacePermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("workspace.id"), nullable=False)


class IndividualDocumentPermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("document.id"), nullable=False)


class IndividualBlockPermission(Base, IndividualObjectPermissionMixin):
    object_id = Column(ForeignKey("block.id"), nullable=False)
