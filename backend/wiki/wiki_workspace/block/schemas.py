from datetime import datetime
from typing import Optional
from uuid import UUID

from wiki.models import WikiBase
from wiki.wiki_workspace.block.enums import TypeBlock
from wiki.wiki_workspace.schemas import ObjectPermissionInfoMixin


class CreateBlock(WikiBase):
    document_id: UUID
    position: int
    type_block: TypeBlock


class UpdateBlockInfo(WikiBase):
    block_id: UUID
    type_block: Optional[TypeBlock] = None
    position: Optional[int] = None


class UpdateBlockData(WikiBase):
    block_id: UUID
    content: str  # WYSIWYG


class BlockInfoResponse(WikiBase, ObjectPermissionInfoMixin):
    id: UUID
    document_id: UUID
    position: int
    type_block: TypeBlock
    created_at: datetime


class WikiLinkSchema(WikiBase):
    workspace_id: Optional[UUID] = None
    document_id: Optional[UUID] = None
    block_id: Optional[UUID] = None

    @classmethod
    def get_from_content_string(cls, content: str):
        """
        Args:
            content: string stored in LakeFS is versioned, format: workspace_id:document_id:block_id
        """
        arr = [None if item == "" else item for item in content.split(":")]
        return cls(workspace_id=UUID(arr[0]),
                   document_id=UUID(arr[1]),
                   block_id=UUID(arr[2]))

    def to_content_string(self):
        return f"{str(self.workspace_id) or ''}:{str(self.document_id) or ''}:{str(self.block_id) or ''}"


class BlockDataResponse(BlockInfoResponse):
    content: str | WikiLinkSchema  # WYSIWYG | data for wiki link
    link: Optional[str] = None
