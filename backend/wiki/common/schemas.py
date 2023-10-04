from pydantic import BaseModel

from wiki.common.exceptions import WikiErrorCode


class WikiErrorResponse(BaseModel):
    """The format of an error response from the Wiki API."""

    error_code: WikiErrorCode
    message: str
