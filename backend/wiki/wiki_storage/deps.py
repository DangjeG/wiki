from lakefs_client.client import LakeFSClient

from wiki.wiki_storage.config import configuration


def get_storage_client() -> LakeFSClient:
    client = LakeFSClient(configuration)
    return client
