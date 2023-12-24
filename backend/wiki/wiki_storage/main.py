from io import StringIO, BufferedReader

from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.base import BaseWikiStorageService

if __name__ == "__main__":
    service = BaseWikiStorageService(get_storage_client())
    res = service.upload_document_block_in_workspace_storage(content=StringIO("content"),
                                                             workspace_id="repo",
                                                             unique_names_parents_documents=["document", "child_document"],
                                                             unique_block_name="block")
    print(res)
