from enum import Enum


class DomainPermissionStatus(str, Enum):
    ACCEPT_APPLICATION = "accept_application"
    ACCEPT_WITHOUT_CONSIDERATION = "accept_without_consideration"
    REFUSE = "refuse"
