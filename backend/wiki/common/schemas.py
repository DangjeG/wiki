from pydantic import BaseModel

from wiki.common.exceptions import WikiErrorCode
from wiki.models import WikiBase


class WikiErrorResponse(BaseModel):
    """The format of an error response from the Wiki API."""

    error_code: WikiErrorCode
    message: str


class BaseResponse(WikiBase):
    status: str = "success"
    msg: str = ""


class HealthCheck(WikiBase):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
