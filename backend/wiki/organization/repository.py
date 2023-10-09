from uuid import UUID

from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import menage_db_not_found_resul_method, NotFoundResultMode
from wiki.organization.models import Organization


class OrganizationRepository(BaseRepository):
    _organization_not_found_exception = WikiException(
        message="User organization not found.",
        error_code=WikiErrorCode.ORGANIZATION_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_not_found_resul_method(NotFoundResultMode.EXCEPTION, ex=_organization_not_found_exception)
    async def get_organization_by_id(self, organization_id: UUID) -> Organization:
        organization_query = await self.session.get(Organization, organization_id)
        return organization_query
