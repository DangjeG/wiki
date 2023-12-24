from io import StringIO
from typing import Optional
from uuid import UUID

from lakefs_client.client import LakeFSClient
from lakefs_client.model.repository_creation import RepositoryCreation

from wiki.config import settings
from wiki.wiki_storage.utils import (
    forming_document_block_storage_path,
    menage_lakefs_api_exception_method
)


class BaseWikiStorageService:
    client: LakeFSClient

    def __init__(self, client: LakeFSClient):
        self.client = client

    @menage_lakefs_api_exception_method()
    def create_workspace_storage(self, workspace_id: UUID) -> dict:
        """
        Creating a new repository in the repository to store workspace data.
        :return: dict {
            'creation_date': timestamp,
            'default_branch': branch_name,
            'id': unique_workspace_name,
            'storage_namespace': 'local://wiki_storage/{unique_workspace_name}'}
        """
        repo = RepositoryCreation(name=str(workspace_id),
                                  storage_namespace=f"{settings.LAKEFS_STORAGE_NAMESPACE_ROOT}{workspace_id}",
                                  default_branch=settings.LAKEFS_DEFAULT_BRANCH)
        thread = self.client.repositories_api.create_repository(repo, async_req=True)
        result = thread.get()

        return result

    @menage_lakefs_api_exception_method()
    def upload_document_block_in_workspace_storage(self,
                                                   content: StringIO,
                                                   workspace_id: UUID,
                                                   document_ids: list[UUID],
                                                   block_id: UUID) -> dict:
        """
        Create a new or update a document block.
        :return: {'checksum': '...',
                  'content_type': '...',
                  'mtime': timestamp,
                  'path': 'document1/.../block1.html',
                  'path_type': 'object',
                  'physical_address': 'local:///home/lakefs/lakefs/data/block/wiki_storage/.../data/.../...',
                  'size_bytes': ...}
        """
        api_instance = self.client.objects_api
        path = forming_document_block_storage_path(document_ids, block_id)
        thread = api_instance.upload_object(repository=str(workspace_id),
                                            branch=str(document_ids[-1]),  # settings.LAKEFS_DEFAULT_BRANCH,
                                            path=path,
                                            content=content,
                                            async_req=True)
        return thread.get()

    @menage_lakefs_api_exception_method()
    def get_content_document_block_in_workspace_storage(self,
                                                        workspace_id: UUID,
                                                        document_ids: list[UUID],
                                                        block_id: UUID,
                                                        version_commit_id: Optional[str]) -> str:
        api_instance = self.client.objects_api
        path = forming_document_block_storage_path(document_ids, block_id)
        thread = api_instance.get_object(repository=str(workspace_id),
                                         ref=version_commit_id or str(document_ids[-1]),  # specific version or latest
                                         path=path,
                                         async_req=True)
        res = thread.get()
        return "".join([item.decode("utf-8") for item in res])
