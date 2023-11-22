from sqlalchemy import Column, Uuid, String, ForeignKey, Boolean
from uuid_extensions import uuid7

from wiki.common.models import DeletedMixin
from wiki.database.core import Base


class Group(Base, DeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String(256), nullable=True)
    is_members_can_add_to_group = Column(Boolean, nullable=False, default=False)


class UserGroup(Base, DeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    group_id = Column(ForeignKey("group.id"), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
