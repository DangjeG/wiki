from typing import Optional
from uuid import UUID

from lakefs_client.model.commit_creation import CommitCreation

from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.wiki_storage.schemas import CommitMetadataScheme
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_storage.utils import forming_document_storage_path, forming_document_block_storage_path


class VersioningWikiStorageService(BaseWikiStorageService):
    def commit_workspace_version(self, unique_workspace_name, metadata: CommitMetadataScheme) -> dict:
        api_instance = self.client.commits_api
        commit_creation = CommitCreation(
            message=utcnow(),
            metadata=metadata.model_dump()
        )
        thread = api_instance.commit(
            unique_workspace_name,
            settings.LAKEFS_DEFAULT_BRANCH,
            commit_creation,
            async_req=True)

        return thread.get()

    def _get_log_commits_workspace(self,
                                   repository: UUID,
                                   amount: Optional[int] = 250,
                                   **kwargs):
        api_instance = self.client.refs_api
        thread = api_instance.log_commits(str(repository),
                                          f"{settings.LAKEFS_DEFAULT_BRANCH}",
                                          amount=amount,
                                          async_req=True,
                                          **kwargs)  # kwargs: prefixes: list[str], objects: list[str]

        return thread.get()

    def get_versions_document(self,
                              workspace_id: UUID,
                              document_ids: list[UUID]):
        path = forming_document_storage_path(document_ids)
        return self._get_log_commits_workspace(workspace_id, prefixes=[path])

    def get_version_document_block(self,
                                   workspace_id: UUID,
                                   document_ids: list[UUID],
                                   block_id: UUID):
        path = forming_document_block_storage_path(document_ids, block_id)
        return self._get_log_commits_workspace(workspace_id, objects=[path])
