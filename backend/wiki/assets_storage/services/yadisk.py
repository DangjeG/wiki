from base64 import b64encode
from io import BytesIO

from yadisk_async import YaDisk
from yadisk_async.common import BinaryAsyncFileLike

from wiki.asset.model import Asset
from wiki.assets_storage.services.base import BaseAssetsStorage
from wiki.assets_storage.utils import manage_ya_disk_storage_exception_method


class YaDiskAssetsStorage(BaseAssetsStorage):

    session: YaDisk

    @manage_ya_disk_storage_exception_method()
    async def upload_asset(self, asset: Asset, data: BytesIO | bytes):
        resource = await self.session.upload(data, self.get_asset_path(asset))
        return await resource.get_download_link()

    @manage_ya_disk_storage_exception_method()
    async def download_asset(self, asset: Asset, is_base64_link: bool = False) -> str:
        if is_base64_link:
            stream = BytesIO()
            await self.session.download(self.get_asset_path(asset), stream)
            base64_asset = b64encode(stream.getvalue()).decode("utf-8")
            return f"data:image/png;base64,{base64_asset}"

        return await self.session.get_download_link(self.get_asset_path(asset))

    @manage_ya_disk_storage_exception_method()
    async def remove_asset(self, asset: Asset):
        await self.session.remove(self.get_asset_path(asset), permanently=True)
