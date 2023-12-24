from sqlalchemy import select

from wiki.user_group.models import Group
from wiki.user_group.schemas import GroupOptionalInfo


def get_group_filters(group_optional_info: GroupOptionalInfo):
    filters = []
    if group_optional_info.name is not None:
        filters.append(select(Group.name.ilike(f"%{group_optional_info.name}%")))
    if group_optional_info.description is not None:
        filters.append(select(Group.description.ilike(f"%{group_optional_info.description}%")))
    if group_optional_info.is_members_can_add_to_group is not None:
        filters.append(select(Group.is_members_can_add_to_group == group_optional_info.is_members_can_add_to_group))

    return filters
