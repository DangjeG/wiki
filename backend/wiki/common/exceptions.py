from enum import IntEnum

from starlette import status


class WikiErrorCode(IntEnum):
    """
        Error codes of the Wiki API.

        Ranges:
               0-1000: general errors
            2000-2999: auth error
            3000-3500: wiki_email error
            3501-3999: permission error
            4000-5000: user errors
            5001-6000: permission errors
            6001-7000: workspace errors
            7001-8000: version errors
            8001-9000: assets storage
        """

    # 0-1000: general errors
    GENERIC_ERROR = 0
    DATABASE_URI_NOT_SET = 1
    API_CLIENT_NOT_AUTHORIZED = 2
    ROOT_TOKEN_NOT_AUTHORIZED = 3
    DATABASE_MAX_RETRIES_EXHAUSTED = 4
    LAKEFS_API_EXCEPTION = 5

    OBJECT_NOT_FOUND = 404

    UNAUTHORIZED_REQUEST = 401
    TOO_MANY_REQUESTS = 429

    # 2000-2999: auth error
    AUTH_NOT_VALIDATE_CREDENTIALS = 2000
    AUTH_API_KEY_NOT_VALID_OR_EXPIRED = 2001
    AUTH_TOKEN_NOT_VALID_OR_EXPIRED = 2002
    AUTH_USER_NOT_FOUND = 2005
    AUTH_API_CLIENT_NOT_FOUND = 2006
    AUTH_NOT_ACCESS = 2005
    AUTH_NOT_EXECUTED = 2006
    AUTH_INSUFFICIENTLY_RESPONSIBILITY = 2007

    # 3000-3500: wiki_email error
    EMAIL_SENDING_ERROR = 3000
    EMAIL_NOT_ALLOWED = 3001

    # 3501-3999: permission error
    PERMISSION_DOMAIN_ERROR = 3501

    # 4000-5000: user errors
    USER_NOT_SPECIFIED = 4000
    USER_DISABLED = 4001
    USER_NOT_FOUND = 4002

    API_CLIENT_NOT_FOUND = 4501
    API_KEY_NOT_FOUND = 4502

    # 5001-6000: permission errors
    PERMISSION_DOMAIN_NOT_FOUND = 5001
    PERMISSION_DOMAIN_NOT_SPECIFIED = 5001

    # 6001-7000: workspace errors
    WORKSPACE_NOT_FOUND = 6001
    WORKSPACE_NOT_SPECIFIED = 6002

    DOCUMENT_NOT_FOUND = 6003
    DOCUMENT_NOT_SPECIFIED = 6004
    DOCUMENT_CURRENT_COMMIT_ALREADY_PUBLISHED = 6005

    BLOCK_NOT_FOUND = 6005
    BLOCK_NOT_SPECIFIED = 6006

    # 7001-8000: version errors
    VERSION_WORKSPACE_NOT_FOUND = 7001
    ROOT_VERSION_WORKSPACE_NOT_FOUND = 7002

    VERSION_DOCUMENT_NOT_FOUND = 7003

    # 8001-9000: assets storage
    ASSET_NOT_FOUND = 8001
    ASSET_LIMIT_SIZE_EXCEEDED_EXCEPTION = 8002
    YA_DISK_API_EXCEPTION = 8003


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
