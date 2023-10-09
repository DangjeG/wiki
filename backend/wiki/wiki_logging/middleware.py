import json
import logging
import math
from typing import Callable

from fastapi import Request, Response
from starlette import status

from wiki.config import settings
from wiki.database.utils import utcnow
from wiki.wiki_logging.schemas import RequestLogSchema


wiki_logger = logging.getLogger("wiki_router_logger")


class WikiRouterLoggerMiddleware:
    EMPTY_VALUE: str = "empty"
    SERVER_PORT = "8000"
    SECRET_PLUG = "secret"

    async def get_protocol(self, request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return self.EMPTY_VALUE

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

    def set_secret_plug(self, data: dict, *keys):
        for key in keys:
            value = data.get(key)
            if value is not None:
                data[key] = self.SECRET_PLUG

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def __call__(
            self,
            request: Request,
            call_next: Callable,
            *args,
            **kwargs
    ):
        start_time = utcnow().timestamp()
        exception_object = None

        # Request Side
        try:
            raw_request_body = await request.body()
            await self.set_body(request, raw_request_body)
            raw_request_body = await self.get_body(request)
            request_body = raw_request_body.decode()
        except Exception:
            request_body = self.EMPTY_VALUE

        server: tuple = request.get("server", ("localhost", self.SERVER_PORT))
        request_headers: dict = dict(request.headers.items())

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            response = Response(
                content=response_body,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())

            # Hiding sensitive data
            self.set_secret_plug(response_headers, "set-cookie", "authorization", settings.AUTH_API_KEY_HEADER_NAME)
            self.set_secret_plug(request_headers, "authorization", "cookie", settings.AUTH_API_KEY_HEADER_NAME)

            response_body = b''
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        duration: int = math.ceil((utcnow().timestamp() - start_time) * 1000)

        request_json_fields = RequestLogSchema(
            request_uri=str(request.url),
            request_referer=request_headers.get("referer", self.EMPTY_VALUE),
            request_protocol=await self.get_protocol(request),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f"{server[0]}:{server[1]}",
            request_size=int(request_headers.get("content-length", 0)),
            request_content_type=request_headers.get("content-type", self.EMPTY_VALUE),
            request_headers=json.dumps(request_headers),
            request_body=request_body,
            request_direction="in",
            remote_ip=request.client[0],
            remote_port=request.client[1],
            response_status_code=response.status_code,
            response_size=int(response_headers.get("content-length", 0)),
            response_headers=json.dumps(response_headers),
            response_body=response_body.decode(),
            duration=duration
        ).model_dump()

        message: str = (f"{'Error' if exception_object else 'Response'} "
                        f"{response.status_code} "
                        f"{request.method} "
                        f"\"{str(request.url)}\" "
                        f"{duration} ms")

        wiki_logger.info(
            message,
            extra={
                "request_json_fields": request_json_fields,
                "to_mask": True
            },
            exc_info=exception_object
        )

        return response
