from abc import ABC, abstractmethod
from io import BytesIO

from wiki.asset.model import Asset


class BaseAssetsStorage(ABC):
    session: object
    storage_base_path: str

    def __init__(self, session, storage_base_path: str = "assets/"):
        self.session = session
        self.storage_base_path = storage_base_path

    @abstractmethod
    async def upload_asset(self, asset: Asset, data: BytesIO):
        pass

    @abstractmethod
    async def download_asset(self, asset: Asset) -> str:
        """
        :returns: Link to download the asset
        """

        pass

    @abstractmethod
    async def remove_asset(self, asset: Asset):
        pass

    def get_asset_path(self, asset: Asset):
        return f"app:/{self.storage_base_path}{str(asset.workspace_id)}/{str(asset.id)}"

    def get_asset_folder_path(self, asset: Asset):
        return f"app:/{self.storage_base_path}{str(asset.workspace_id)}/"
