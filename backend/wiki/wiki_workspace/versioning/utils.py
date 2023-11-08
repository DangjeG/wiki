from datetime import datetime
from functools import wraps
from typing import Optional
from uuid import UUID

from lakefs_client import ApiException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.user.utils import get_user_info
from wiki.wiki_workspace.block.model import Block
from wiki.wiki_workspace.document.model import Document
from wiki.wiki_workspace.versioning.schemas import VersionBlockInfo, VersionDocumentInfo


async def get_version_block_info_list(results: dict, block: Block, session: AsyncSession) -> list[VersionBlockInfo]:
    """
    :param results: Result get from the dictionary from lakefs answer
    :param block: Versioning block
    :param session: Database session
    """

    return [VersionBlockInfo(
        commit_id=item.get("id"),
        object_id=block.id,
        committer_user=await get_user_info(UUID(item.get("metadata").get("committer_user_id")), session, is_full=False),
        created_at=datetime.fromtimestamp(int(item.get("creation_date")))
    ) for item in results]


async def get_version_document_info_list(results: dict, document: Document, session: AsyncSession) -> list[VersionDocumentInfo]:
    """
    :param results: Result get from the dictionary from lakefs answer
    :param document: Versioning document
    :param session: Database session
    """

    return [VersionDocumentInfo(
        commit_id=item.get("id"),
        object_id=document.id,
        committer_user=await get_user_info(UUID(item.get("metadata").get("committer_user_id")), session, is_full=False),
        created_at=datetime.fromtimestamp(int(item.get("creation_date"))),
        is_published=item.get("id") == document.current_published_version_commit_id
    ) for item in results]
