from enum import IntEnum

from starlette import status


class WikiErrorCode(IntEnum):
    """
        Error codes of the Wiki API.

        Ranges:
            0-1000: general errors
            3000-3999: email error
            4000-5000: user errors
        """

    # 0-1000: general errors
    GENERIC_ERROR = 0

    OBJECT_NOT_FOUND = 404

    UNAUTHORIZED_REQUEST = 401
    TOO_MANY_REQUESTS = 429

    # 3000-3999: email error
    EMAIL_SENDING_ERROR = 3000

    # 4000-5000: user errors
    USER_NOT_SPECIFIED = 4000
    USER_DISABLED = 4001
    USER_NOT_FOUND = 4002


class WikiException(Exception):
    """Base class for Wiki exceptions."""

    message: str
    error_code: int
    http_status_code: status

    def __init__(self,
                 message: str,
                 error_code: WikiErrorCode,
                 http_status_code: status = status.HTTP_400_BAD_REQUEST,
                 *args):
        super().__init__(message, error_code, http_status_code, *args)
        self.message = message
        self.error_code = error_code
        self.http_status_code = http_status_code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(message='{self.message}', error_code={self.error_code}, http_status_code={self.http_status_code})"
