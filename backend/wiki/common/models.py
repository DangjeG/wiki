from sqlalchemy import Column, DateTime, event, Boolean

from wiki.database.utils import utcnow


class TimeStampMixin:
    """Timestamping mixin"""

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


class DeletedMixin(TimeStampMixin):
    is_deleted = Column(Boolean, nullable=False, default=False)


class EnabledDeletedMixin(DeletedMixin):
    is_enabled = Column(Boolean, nullable=False, default=True)
