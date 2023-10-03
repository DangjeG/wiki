from sqlalchemy.orm import relationship
from uuid_extensions.uuid7 import uuid7
from wiki.models.base import Base
from sqlalchemy import Column, String, ForeignKey


class User(Base):
    __tablename__ = 'user'

    id = Column(default=uuid7, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)
    account_id = Column(ForeignKey("account.id"), default=uuid7, unique=True)

    account = relationship('Account', back_populates="user")

    def __init__(self,
                 email: str,
                 user_name: str,
                 display_name: str,
                 first_name: str,
                 last_name: str,
                 account_id: str,
                 second_name: str = None):
        self.email = email
        self.user_name = user_name
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.second_name = second_name
        self.account_id = account_id
