from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_api_client.models import WikiApiClient


class CreateWorkspace(WikiBase):
    title: str
    owner: WikiApiClient


class WorkspaceResponse(WikiBase):
    title: str


class WorkspaceInfo(WikiBase):
    id: UUID
    title: str
    owner: WikiApiClient
