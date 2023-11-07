from typing import Optional
from uuid import UUID

from lakefs_client.model.branch_creation import BranchCreation
from lakefs_client.model.cherry_pick_creation import CherryPickCreation
from lakefs_client.model.commit import Commit
from lakefs_client.model.commit_creation import CommitCreation
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.wiki_storage.schemas import CommitMetadataScheme
from wiki.wiki_storage.services.base import BaseWikiStorageService
from wiki.wiki_storage.utils import forming_document_storage_path, forming_document_block_storage_path
from wiki.wiki_workspace.versioning.utils import menage_lakefs_api_exception_method


class VersioningWikiStorageService(BaseWikiStorageService):

    @menage_lakefs_api_exception_method()
    def commit_workspace_document_version(self,
                                          workspace_id: UUID,
                                          document_id: UUID,
                                          metadata: CommitMetadataScheme) -> dict:
        api_instance = self.client.commits_api
        commit_creation = CommitCreation(
            message=str(utcnow()),
            metadata=metadata.model_dump()
        )
        thread = api_instance.commit(
            str(workspace_id),
            str(document_id),
            commit_creation,
            async_req=True
        )

        return thread.get()

    @menage_lakefs_api_exception_method()
    def create_branch_for_workspace_document(self, workspace_id: UUID, document_id: UUID) -> dict:
        """
        Create a new branch to store the data of each individual document. The default source branch is main.
        """
        api_instance = self.client.branches_api
        branch_creation = BranchCreation(
            name=str(document_id),
            source=settings.LAKEFS_DEFAULT_BRANCH,
        )
        thread = api_instance.create_branch(str(workspace_id), branch_creation, async_req=True)

        return thread.get()

    @menage_lakefs_api_exception_method()
    def rollback_document(self,
                          workspace_id: UUID,
                          document_id: UUID,
                          commit_id: str,
                          metadata: CommitMetadataScheme) -> Commit:
        api_instance = self.client.branches_api
        cherry_pick_creation = CherryPickCreation(ref=commit_id, metadata=metadata.model_dump())
        thread = api_instance.cherry_pick(repository=str(workspace_id),
                                          branch=str(document_id),
                                          cherry_pick_creation=cherry_pick_creation,
                                          async_req=True)
        return thread.get()

    @menage_lakefs_api_exception_method()
    def _get_log_commits_workspace_document(self,
                                            repository_id: UUID,
                                            branch_id: UUID,
                                            amount: Optional[int] = 250,
                                            **kwargs):
        api_instance = self.client.refs_api
        thread = api_instance.log_commits(str(repository_id),
                                          str(branch_id),
                                          amount=amount,
                                          async_req=True,
                                          **kwargs)  # kwargs: prefixes: list[str], objects: list[str]

        return thread.get()

    def get_versions_document(self,
                              workspace_id: UUID,
                              document_ids: list[UUID]):
        path = forming_document_storage_path(document_ids)
        return self._get_log_commits_workspace_document(workspace_id, document_ids[-1], prefixes=[path])

    def get_version_document_block(self,
                                   workspace_id: UUID,
                                   document_ids: list[UUID],
                                   block_id: UUID):
        path = forming_document_block_storage_path(document_ids, block_id)
        return self._get_log_commits_workspace_document(workspace_id, document_ids[-1], objects=[path])

    commits_not_found_exception = WikiException(
        message="The requested document, has not yet been saved at any time. Commits not found.",
        error_code=WikiErrorCode.VERSION_DOCUMENT_NOT_FOUND,
        http_status_code=status.HTTP_409_CONFLICT
    )

    @menage_lakefs_api_exception_method(commits_not_found_exception)
    def get_current_version_document_commit_id(self,
                                               workspace_id: UUID,
                                               document_ids: list[UUID]):
        api_instance = self.client.branches_api
        thread = api_instance.get_branch(str(workspace_id), str(document_ids[-1]), async_req=True)

        return thread.get()
