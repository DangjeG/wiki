from typing import Optional

from sqlalchemy import Column, String, Uuid, Boolean, ForeignKey
from uuid_extensions import uuid7

from wiki.common.models import TimeStampMixin, EnabledDeletedMixin
from wiki.database.core import Base


class User(Base, EnabledDeletedMixin):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=True)
    display_name = Column(String, nullable=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)

    position = Column(String, nullable=True)

    is_user_agreement_accepted = Column(Boolean, nullable=False, default=False)
    is_verified_email = Column(Boolean, nullable=False, default=False)

    organization_id = Column(ForeignKey("organization.id"), nullable=False)
    wiki_api_client_id = Column(ForeignKey("wiki_api_client.id"), nullable=True)

    def __init__(self,
                 email: str,
                 first_name: str,
                 last_name: str,
                 display_name: Optional[str] = None,
                 username: Optional[str] = None,
                 second_name: Optional[str] = None,
                 position: Optional[str] = None,
                 is_user_agreement_accepted: bool = False,
                 organization_id: Optional[str] = None,
                 wiki_api_client_id: Optional[str] = None):
        self.email = email
        self.username = username
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.second_name = second_name
        self.position = position
        self.is_user_agreement_accepted = is_user_agreement_accepted
        self.organization_id = organization_id
        self.wiki_api_client_id = wiki_api_client_id
