from uuid import UUID

from wiki.wiki_workspace.block.model import TypeBlock
from wiki.wiki_workspace.block.schemas import CreateBlock


def get_template_first_block(document_id: UUID) -> CreateBlock:
    return CreateBlock(
        document_id=document_id,
        position=0,
        type_block=TypeBlock.TEXT
    )
