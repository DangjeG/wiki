from abc import ABC

from starlette import status

from wiki.auth.enums import AuthorizationMode
from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.common.schemas import ExternalUserHandlerData, WikiUserHandlerData
from wiki.wiki_api_client.enums import ResponsibilityType


class _AuthorizationPermission(ABC):
    authorisation_mode: AuthorizationMode

    def __init__(self,
                 authorisation_mode: AuthorizationMode = AuthorizationMode.AUTHORIZED):
        self.authorisation_mode = authorisation_mode

    def __call__(self, user: ExternalUserHandlerData | WikiUserHandlerData):
        if self.authorisation_mode > user.authorisation_status:
            raise WikiException(
                message="You must authorization.",
                error_code=WikiErrorCode.AUTH_NOT_EXECUTED,
                http_status_code=status.HTTP_403_FORBIDDEN
            )


class _ResponsibilityPermission(ABC):
    responsibility: ResponsibilityType

    def __init__(self,
                 responsibility: ResponsibilityType = ResponsibilityType.VIEWER):
        self.responsibility = responsibility

    def __call__(self, user: WikiUserHandlerData):
        if not isinstance(user, WikiUserHandlerData) or self.responsibility > user.wiki_api_client.responsibility:
            raise WikiException(
                message="You have insufficiently responsibility.",
                error_code=WikiErrorCode.AUTH_INSUFFICIENTLY_RESPONSIBILITY,
                http_status_code=status.HTTP_403_FORBIDDEN
            )


class BasePermission(_AuthorizationPermission, _ResponsibilityPermission):
    """
    Base permission class. Note: if unauthorized mode is specified, responsibility will not be checked.
    """

    def __init__(self,
                 authorisation_mode: AuthorizationMode = AuthorizationMode.AUTHORIZED,
                 responsibility: ResponsibilityType = ResponsibilityType.VIEWER):
        _AuthorizationPermission.__init__(authorisation_mode)
        _ResponsibilityPermission.__init__(responsibility)

    def __call__(self, user: ExternalUserHandlerData | WikiUserHandlerData):
        _AuthorizationPermission.__call__(user)
        if self.authorisation_mode != AuthorizationMode.UNAUTHORIZED:
            _ResponsibilityPermission.__call__(user)
