from uuid_extensions import uuid7

from wiki.wiki_storage.deps import get_storage_client
from wiki.wiki_storage.services.creation import CreationWikiStorageService

if __name__ == "__main__":
    service = CreationWikiStorageService(get_storage_client())
    service.create_workspace_storage(uuid7())
