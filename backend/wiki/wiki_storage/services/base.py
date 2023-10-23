from lakefs_client.client import LakeFSClient


class BaseWikiStorageService:
    client: LakeFSClient

    def __init__(self, client: LakeFSClient):
        self.client = client
