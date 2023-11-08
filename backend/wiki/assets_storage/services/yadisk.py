from io import BytesIO

from yadisk_async import YaDisk

from wiki.asset.model import Asset
from wiki.assets_storage.services.base import BaseAssetsStorage
from wiki.assets_storage.utils import manage_ya_disk_storage_exception_method


class YaDiskAssetsStorage(BaseAssetsStorage):

    session: YaDisk

    @manage_ya_disk_storage_exception_method()
    async def upload_asset(self, asset: Asset, data: BytesIO):
        resource = await self.session.upload(data, self.get_asset_path(asset))
        return await resource.get_download_link()

    @manage_ya_disk_storage_exception_method()
    async def download_asset(self, asset: Asset) -> str:
        bytes_io = BytesIO()
        resource = await self.session.download(self.get_asset_path(asset), bytes_io)
        return await resource.get_download_link()

    @manage_ya_disk_storage_exception_method()
    async def remove_asset(self, asset: Asset):
        await self.session.remove(self.get_asset_path(asset), permanently=True)
