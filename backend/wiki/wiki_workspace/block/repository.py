from typing import Optional
from uuid import UUID

from sqlalchemy import select, and_
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.database.utils import (
    CommitMode,
    menage_db_commit_method,
    menage_db_not_found_result_method,
    NotFoundResultMode
)
from wiki.permissions.object.general.models import GeneralBlockPermission
from wiki.permissions.object.group.models import GroupBlockPermission
from wiki.permissions.object.individual.models import IndividualBlockPermission
from wiki.wiki_workspace.block.enums import TypeBlock
from wiki.wiki_workspace.block.model import Block, VersionBlock
from wiki.wiki_workspace.block.schemas import CreateBlock
from wiki.wiki_workspace.repository import ObjectRepository


class BlockRepository(ObjectRepository):
    block_not_found_exception = WikiException(
        message="Block not found.",
        error_code=WikiErrorCode.BLOCK_NOT_FOUND,
        http_status_code=status.HTTP_404_NOT_FOUND
    )

    async def _get_result_block_with_permission(self,
                                                user_id: UUID, *whereclause,
                                                version_commit_id: Optional[str] = None):
        return await self._get_result_object_with_permission(
            Block,
            IndividualBlockPermission,
            GroupBlockPermission,
            GeneralBlockPermission,
            user_id,
            version_commit_id,
            *whereclause
        )

    async def get_blocks_with_permission(self,
                                         user_id: UUID,
                                         version_commit_id: Optional[str] = None) -> list:
        whereclause = []
        if version_commit_id is None:
            whereclause.append(Block.is_deleted == False)
        res = await self._get_result_block_with_permission(user_id,
                                                           version_commit_id=version_commit_id,
                                                           *whereclause)
        return res.all()

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=block_not_found_exception)
    async def get_block_with_permission_by_id(self,
                                              user_id: UUID,
                                              block_id: UUID,
                                              version_commit_id: Optional[str] = None):
        whereclause = [Block.id == block_id]
        if version_commit_id is None:
            whereclause.append(Block.is_deleted == False)
        res = await self._get_result_block_with_permission(user_id,
                                                           version_commit_id=version_commit_id,
                                                           *whereclause)
        return res.first()

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
    async def create_version_block(self, block: Block, version_commit_id: str) -> VersionBlock:
        new_version_block = VersionBlock(
            block_id=block.id,
            version_commit_id=version_commit_id
        )

        self.session.add(new_version_block)

        return new_version_block

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_block(self,
                           block_id: UUID,
                           *,
                           position: Optional[int] = None,
                           type_block: Optional[TypeBlock] = None) -> Block:
        block = await self.get_block_by_id(block_id)
        if position is not None:
            block.position = position
        if type_block is not None:
            block.type_block = str(type_block)
        self.session.add(block)

        return block

    @menage_db_commit_method(CommitMode.FLUSH)
    async def mark_block_deleted(self, block_id: UUID):
        block = await self.get_block_by_id(block_id)
        block.is_deleted = True
        self.session.add(block)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def mark_block_undeleted(self, block_id: UUID):
        block = await self.get_block_by_id(block_id, is_only_existing=False)
        block.is_deleted = False
        self.session.add(block)

    async def get_all_block_with_permissions_by_document_id(self,
                                                            user_id: UUID,
                                                            document_id: UUID,
                                                            version_commit_id: Optional[str] = None):
        whereclause = [Block.document_id == document_id]
        if version_commit_id is None:
            whereclause.append(Block.is_deleted == False)
        res = await self._get_result_block_with_permission(user_id,
                                                           version_commit_id=version_commit_id,
                                                           *whereclause)
        return res.all()

    async def get_all_block_by_document_id(self,
                                           document_id: UUID,
                                           version_commit_id: Optional[str] = None) -> list[Block]:
        whereclause = [Block.document_id == document_id]
        st = select(Block)
        if version_commit_id is None:
            whereclause.append(Block.is_deleted == False)
        else:
            st = st.join(VersionBlock, Block.id == VersionBlock.block_id)
            whereclause.append(VersionBlock.version_commit_id == version_commit_id)
        block_query = await self.session.execute(st.where(and_(*whereclause)).order_by(Block.position))
        result = block_query.scalars().all()
        return result

    @menage_db_not_found_result_method(NotFoundResultMode.EXCEPTION, ex=block_not_found_exception)
    async def get_block_by_id(self, block_id: UUID, is_only_existing: bool = True) -> Block:
        whereclause = [Block.id == block_id]
        if is_only_existing:
            whereclause.append(Block.is_deleted == False)
        st = select(Block).where(and_(*whereclause))
        block_query = (await self.session.execute(st)).scalar()
        return block_query
