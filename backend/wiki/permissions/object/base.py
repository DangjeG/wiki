from sqlalchemy import Column, Uuid, String
from uuid_extensions import uuid7

from wiki.common.models import TimeStampMixin
from wiki.permissions.object.enums import ObjectPermissionMode


class BaseObjectPermissionMixin(TimeStampMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    mode = Column(String, nullable=False, default=str(ObjectPermissionMode.HIDDEN_INACCESSIBLE))
    object_id: Column
