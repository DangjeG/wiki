from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_workspace.block.model import TypeBlock


class CreateBlock(WikiBase):
    document_id: UUID
    workspace_id: UUID
    type_block: TypeBlock

class BlockInfo(WikiBase):
    document_id: UUID
    workspace_id: UUID
    type_block: TypeBlock
