from sqlalchemy.orm import relationship
from uuid_extensions.uuid7 import uuid7
from sqlalchemy import Column, String

from wiki.models.base import Base
from wiki.auth.models.enums.provider_type import ProviderType


class Account(Base):
    __tablename__ = 'account'

    id = Column(default=uuid7, primary_key=True, nullable=False)
    provider_type = Column(default=ProviderType, nullable=False)
    provider_value = Column(String, nullable=False)

    user = relationship('User', back_populates="account")

    def __init__(self,
                 provider_type: ProviderType,
                 provider_value: str):
        self.provider_type = provider_type
        self.provider_type = provider_value
