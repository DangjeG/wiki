from uuid import UUID

from wiki.database.repository import BaseRepository
from wiki.database.utils import CommitMode, menage_db_commit_method
from wiki.wiki_workspace.block.model import Block
from wiki.wiki_workspace.block.schemas import CreateBlock


class BlockRepository(BaseRepository):
    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_block(self, create_block: CreateBlock) -> Block:
        new_block = Block(
            document_id=create_block.document_id,
            workspace_id=create_block.workspace_id,
            type_block=create_block.type_block
        )

        self.session.add(new_block)

        return new_block

    async def get_all_block_by_document_id(self, document_id: UUID) -> list[Block]:
        block_query = await self.session.get(Block, document_id)
        result = block_query.scalars().all()
        return result
