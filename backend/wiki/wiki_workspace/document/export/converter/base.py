from abc import ABC, abstractmethod
from io import BytesIO


class BaseConverter(ABC):

    @abstractmethod
    def convert(self, source: str | bytes | BytesIO) -> bytes:
        ...
