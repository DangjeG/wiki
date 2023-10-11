from enum import Enum


class OrganizationAccessType(str, Enum):
    FULL_ACCESS = "FULL_ACCESS"
    WEB_ONLY = "WEB_ONLY"
    LOCKED = "LOCKED"
