from enum import Enum


class ResponsibilityType(str, Enum):
    VIEWER = "VIEWER",
    EDITOR = "EDITOR",
    ADMIN = "ADMIN"
