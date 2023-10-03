import enum

class ProviderType(str, enum.Enum):
    email = "email",
    google = "google",
