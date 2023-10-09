from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, or_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    menage_db_not_found_resul_method,
    NotFoundResultMode,
    menage_db_commit_method,
    CommitMode,
    DELETED_USER_DISPLAY_NAME,
    DELETED_USER_ID_PREFIX,
    DELETED_USER_EMAIL_HOST,
    DELETED_USER_FIRST_NAME,
    DELETED_USER_LAST_NAME,
    DELETED_USER_SECOND_NAME
)
from wiki.user.models import User
from wiki.user.schemas import CreateUser


class UserRepository(BaseRepository):
    _user_not_found_exception = WikiException(
        message="User not found.",
        error_code=WikiErrorCode.USER_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )
    _user_forbidden_exception = WikiException(
        message="API key is not valid or expired.",
        error_code=WikiErrorCode.AUTH_API_KEY_NOT_VALID_OR_EXPIRED,
        http_status_code=status.HTTP_403_FORBIDDEN
    )

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_user_not_found_exception)
    async def get_user_by_id(self, user_id: UUID) -> User:
        user_query = await self.session.get(User, user_id)
        return user_query

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_user_not_found_exception)
    async def get_user_by_email(self, email: str) -> User:
        st = select(User).where(User.email == email)
        user_query = (await self.session.execute(st)).scalar()
        return user_query

    async def check_user_identification_data_is_available(self, email: str, username: Optional[str]) -> bool:
        st = select(func.count(User.id)).where(or_(User.email == email, User.username == username))
        count = (await self.session.execute(st)).scalar()
        return not count > 0

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_user_forbidden_exception)
    async def get_user_by_wiki_api_client_id(self, api_client_id: UUID) -> User:
        st = select(User).where(User.wiki_api_client_id == api_client_id)
        user_query = (await self.session.execute(st)).scalar()
        return user_query

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_user_not_found_exception)
    async def get_user_by_username(self, username: str) -> User:
        st = select(User).where(User.username == username)
        user_query = (await self.session.execute(st)).scalar()
        return user_query

    async def get_all_users(self) -> list[User]:
        users_query = await self.session.execute(select(User))
        res = users_query.scalars().all()
        return res

    @menage_db_commit_method(CommitMode.COMMIT)
    async def create_user(self, create_user: CreateUser) -> User:
        new_user = User(
            email=create_user.email,
            username=create_user.username,
            display_name=create_user.display_name,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            second_name=create_user.second_name,
            position=create_user.position,
            organization_id=create_user.organization_id
        )

        self.session.add(new_user)

        return new_user

    @menage_db_commit_method(CommitMode.COMMIT)
    async def update_user(self,
                          user_id: UUID,
                          *,
                          email: Optional[str] = None,
                          username: Optional[str] = None,
                          display_name: Optional[str] = None,
                          first_name: Optional[str] = None,
                          last_name: Optional[str] = None,
                          second_name: Optional[str] = None,
                          position: Optional[str] = None,
                          organization_id: Optional[UUID] = None,
                          wiki_api_client_id: Optional[str] = None) -> User:
        user: User = await self.get_user_by_id(user_id)
        if email is not None:
            user.email = email
        if username is not None:
            user.username = username
        if display_name is not None:
            user.display_name = display_name
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if second_name is not None:
            user.second_name = second_name
        if position is not None:
            user.position = position
        if organization_id is not None:
            user.organization_id = organization_id
        if wiki_api_client_id is not None:
            user.wiki_api_client_id = wiki_api_client_id

        self.session.add(user)

        return user

    @menage_db_commit_method(CommitMode.COMMIT)
    async def mark_user_deleted(self, user_id: UUID) -> None:
        user: User = await self.get_user_by_id(user_id)

        user.is_deleted = True
        user.display_name = DELETED_USER_DISPLAY_NAME
        user.email = f"{user.id}@{DELETED_USER_EMAIL_HOST}"
        user.username = f"{DELETED_USER_ID_PREFIX}{user.id}"
        user.first_name = DELETED_USER_FIRST_NAME
        user.last_name = DELETED_USER_LAST_NAME
        user.second_name = DELETED_USER_SECOND_NAME

        self.session.add(user)
