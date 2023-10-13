import asyncio
import random
import warnings
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from wiki.database.deps import db_metadata_create_all, get_db
from wiki.database.utils import utcnow
from wiki.organization.enums import OrganizationAccessType
from wiki.organization.models import Organization
from wiki.organization.repository import OrganizationRepository
from wiki.organization.schemas import CreateOrganization
from wiki.permissions.domain.enums import DomainPermissionMode
from wiki.permissions.domain.models import PermissionDomain
from wiki.permissions.domain.repository import PermissionDomainRepository
from wiki.permissions.domain.schemas import CreatePermissionDomain
from wiki.user.models import User
from wiki.user.repository import UserRepository
from wiki.user.schemas import CreateUser
from wiki.wiki_api_client.enums import ResponsibilityType
from wiki.wiki_api_client.models import WikiApiClient
from wiki.wiki_api_client.repository import WikiApiClientRepository
from wiki.wiki_api_client.schemas import CreateWikiApiClient


# async def get_db():
#     session: AsyncSession = get_session()
#     async with session.begin() as transaction:
#         return session


async def init_db():
    await db_metadata_create_all()


def generate_hex(length: int):
    hex_chars = '0123456789abcdef'
    hex_sequence = ''
    for _ in range(length):
        hex_sequence += random.choice(hex_chars)
    return hex_sequence


async def gen_random_users(session: AsyncSession, count: int):
    permission_domain_repo: PermissionDomainRepository = PermissionDomainRepository(session)
    organization_repository: OrganizationRepository = OrganizationRepository(session)
    user_repo: UserRepository = UserRepository(session)
    for _ in range(count):
        yield await _gen_random_user(permission_domain_repo,
                                     organization_repository,
                                     user_repo)


async def _gen_random_user(permission_domain_repo: PermissionDomainRepository,
                           organization_repository: OrganizationRepository,
                           user_repo: UserRepository):
    permission_domains: list[PermissionDomain] = await permission_domain_repo.get_all_permission_domains()
    if len(permission_domains) < 1:
        raise Exception("No resolved domains for email were found.")

    organizations: list[Organization] = await organization_repository.get_all_organization()
    if len(organizations) < 1:
        raise Exception("Can't find any organizations.")

    user_repo: UserRepository
    new_user: User = await user_repo.create_user(CreateUser(
        email=f"{uuid7().hex}@{random.choice(permission_domains).domain}",
        username=uuid7().hex,
        first_name="gen first name",
        last_name="gen last name",
        second_name="gen second name",
        position="gen position",
        is_user_agreement_accepted=True,
        organization_id=random.choice(organizations).id
    ))

    return new_user


async def verify_and_trust_user(user: User,
                                api_client_repository: WikiApiClientRepository,
                                user_repo: UserRepository,
                                responsibility: Optional[ResponsibilityType] = None):
    if user.wiki_api_client_id is not None:
        warnings.warn(f"User {user.id} is already trusted.")
        return
    if responsibility is None:
        responsibility = random.choice(list(ResponsibilityType))
    new_api_client: WikiApiClient = await api_client_repository.create_wiki_api_client(CreateWikiApiClient(
        description="gen description",
        responsibility=responsibility,
        is_enabled=True
    ))
    await user_repo.update_user(user.id, is_verified_email=True, wiki_api_client_id=new_api_client.id)


async def gen_verified_and_trust_user(session: AsyncSession, count: int):
    print(f"Start gen verified and trust user [{count}]")
    api_client_repository: WikiApiClientRepository = WikiApiClientRepository(session)
    user_repo: UserRepository = UserRepository(session)
    async for new_user in gen_random_users(session, count):
        await verify_and_trust_user(new_user, api_client_repository, user_repo)


async def _gen_permission_domain(permission_domain_repo: PermissionDomainRepository):
    await permission_domain_repo.create_permission_domain(CreatePermissionDomain(
        domain=f"{uuid7().hex}.com",
        mode=DomainPermissionMode.ACCEPT
    ))


async def gen_permission_domains(session: AsyncSession, count: int):
    print(f"Start gen permission domains [{count}]")
    for _ in range(count):
        await _gen_permission_domain(PermissionDomainRepository(session))


async def _gen_organization(organization_repository: OrganizationRepository):
    await organization_repository.create_organization(CreateOrganization(
        name="gen organization",
        description="gen description",
        access=OrganizationAccessType.FULL_ACCESS
    ))


async def gen_organizations(session: AsyncSession, count: int):
    print(f"Start gen organisations [{count}]")
    organization_repository: OrganizationRepository = OrganizationRepository(session)
    for _ in range(count):
        await _gen_organization(organization_repository)


async def init_test_db():
    await init_db()
    async for session in get_db():
        await gen_permission_domains(session, 20)
        await gen_organizations(session, 20)
        await gen_verified_and_trust_user(session, 50)


if __name__ == "__main__":
    print(f"Start generation - {utcnow()}")
    asyncio.run(init_test_db())
    print(f"Generation complete!")
