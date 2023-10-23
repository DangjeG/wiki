from lakefs_client.model.repository_creation import RepositoryCreation

from wiki.config import settings
from wiki.wiki_storage.services.base import BaseWikiStorageService


class CreationWikiStorageService(BaseWikiStorageService):
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
