from io import IOBase

from lakefs_client.client import LakeFSClient
from lakefs_client.model.repository_creation import RepositoryCreation

from wiki.config import settings
from wiki.wiki_storage.utils import forming_document_storage_path


class BaseWikiStorageService:
    client: LakeFSClient

    def __init__(self, client: LakeFSClient):
        self.client = client

    def create_workspace_storage(self, unique_workspace_name) -> dict:
        """
        Creating a new repository in the repository to store workspace data.
        :return: dict {
            'creation_date': timestamp,
            'default_branch': branch_name,
            'id': unique_workspace_name,
            'storage_namespace': 'local://wiki_storage/{unique_workspace_name}'}
        """
        repo = RepositoryCreation(name=unique_workspace_name,
                                  storage_namespace=f"{settings.LAKEFS_STORAGE_NAMESPACE_ROOT}{unique_workspace_name}",
                                  default_branch=settings.LAKEFS_DEFAULT_BRANCH)
        thread = self.client.repositories_api.create_repository(repo, async_req=True)
        result = thread.get()

        return result

    def upload_document_block_in_workspace_storage(self,
                                                   content: IOBase,
                                                   unique_workspace_name: str,
                                                   unique_names_parents_documents: list[str],
                                                   unique_block_name: str) -> dict:
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
        path = forming_document_storage_path(unique_names_parents_documents, unique_block_name)
        thread = api_instance.upload_object(repository=unique_workspace_name,
                                            branch=settings.LAKEFS_DEFAULT_BRANCH,
                                            path=path,
                                            content=content,
                                            async_req=True)
        return thread.get()

    def get_content_document_block_in_workspace_storage(self,
                                                        unique_workspace_name: str,
                                                        unique_names_parents_documents: list[str],
                                                        unique_block_name: str) -> str:
        api_instance = self.client.objects_api
        path = forming_document_storage_path(unique_names_parents_documents, unique_block_name)
        thread = api_instance.get_object(repository=unique_workspace_name,
                                         ref=settings.LAKEFS_DEFAULT_BRANCH,
                                         path=path,
                                         async_req=True)
        res = thread.get()
        return "".join([item.decode("utf-8") for item in res])
