from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.repository import BaseRepository
from wiki.database.utils import (
    CommitMode,
    menage_db_commit_method,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.wiki_workspace.block.model import Block
from wiki.wiki_workspace.block.schemas import CreateBlock


class BlockRepository(BaseRepository):
    _block_not_found_exception = WikiException(
        message="Block not found.",
        error_code=WikiErrorCode.BLOCK_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_block(self, create_block: CreateBlock) -> Block:
        new_block = Block(
            document_id=create_block.document_id,
            position=create_block.position,
            type_block=str(create_block.type_block)
        )

        self.session.add(new_block)

        return new_block

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_block(self,
                           block_id: UUID,
                           *,
                           position: Optional[int] = None) -> Block:
        block = await self.get_block_by_id(block_id)
        if position is not None:
            block.position = position
        self.session.add(block)

        return block

    @menage_db_commit_method(CommitMode.FLUSH)
    async def mark_block_deleted(self, block_id: UUID):
        block = await self.get_block_by_id(block_id)
        block.is_deleted = True
        self.session.add(block)

    async def get_all_block_by_document_id(self,
                                           document_id: UUID,
                                           is_only_existing: bool = True) -> list[Block]:
        whereclause = [Block.document_id == document_id]
        if is_only_existing:
            whereclause.append(Block.is_deleted == False)
        block_query = await self.session.execute(select(Block).where(and_(*whereclause)).order_by(Block.position))
        result = block_query.scalars().all()
        return result

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=_block_not_found_exception)
    async def get_block_by_id(self, block_id: UUID, is_only_existing: bool = True) -> Block:
        whereclause = [Block.id == block_id]
        if is_only_existing:
            whereclause.append(Block.is_deleted == False)
        st = select(Block).where(and_(*whereclause))
        block_query = (await self.session.execute(st)).scalar()
        return block_query
