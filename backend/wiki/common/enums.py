from enum import Enum
from functools import total_ordering


@total_ordering
class WikiBaseEnum(Enum):
    def __le__(self, other):
        members = list(self.__class__.__members__.values())
        return members.index(self) <= members.index(other)

    def __str__(self):
        return self.value
