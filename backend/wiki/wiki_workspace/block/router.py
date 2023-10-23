from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.schemas import BaseResponse
from wiki.database.deps import get_db
from wiki.wiki_workspace.block.repository import BlockRepository
from wiki.wiki_workspace.block.schemas import CreateBlock, BlockInfo

block_router = APIRouter()

@block_router.post(
    "/block",
    response_model=BaseResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create block."
)
async def create_block(
        new_block: CreateBlock,
        session: AsyncSession = Depends(get_db)):
    block_repository: BlockRepository = BlockRepository(session)

    await block_repository.create_block(new_block)

    return BaseResponse(
        msg="Block created."
    )

@block_router.get(
    "/block",
    response_model=list[BlockInfo],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get all block by id document."
)
async def get_blocks(document_id: UUID,
                     session: AsyncSession = Depends(get_db)):
    block_repository: BlockRepository = BlockRepository(session)

    blocks = await block_repository.get_all_block_by_document_id(document_id=document_id)

    result_blocks: list[BlockInfo] = []
    for block in blocks:
        append_block = BlockInfo(
            document_id=block.document_id,
            workspace_id=block.workspace_id,
            type_block=block.type_block
        )
        result_blocks.append(append_block)

    return result_blocks
