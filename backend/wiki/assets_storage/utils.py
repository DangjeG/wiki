from functools import wraps

from starlette import status
from yadisk_async import YaDisk
from yadisk_async.exceptions import ParentNotFoundError, YaDiskError

from wiki.asset.model import Asset
from wiki.common.exceptions import WikiException, WikiErrorCode


def manage_ya_disk_storage_exception_method():
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            try:
                result = await f(self, *args, **kwargs)
                return result
            except ParentNotFoundError as ex:
                session: YaDisk = self.session
                asset: Asset = args[0]
                await session.mkdir(self.get_asset_folder_path(asset))
                result = await f(self, *args, **kwargs)
                return result
            except YaDiskError as ex:
                raise WikiException(
                    message=ex.error_type,
                    error_code=WikiErrorCode.YA_DISK_API_EXCEPTION,
                    http_status_code=status.HTTP_400_BAD_REQUEST
                )

        return wrapped_f

    return decorator
