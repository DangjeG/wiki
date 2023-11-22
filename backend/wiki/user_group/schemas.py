from typing import Optional

from wiki.models import WikiBase


class GroupFilter(WikiBase):
    name: Optional[str] = None
    description: Optional[str] = None
