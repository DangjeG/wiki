from uuid_extensions import uuid7

from wiki.common.schemas import WikiUserHandlerData, FakeWikiApiClient


def get_fake_admin_user_handler_data() -> WikiUserHandlerData:
    user_id = uuid7()
    return WikiUserHandlerData(
        id=user_id,
        email=f"{user_id.hex}@{user_id.hex}.com",
        username=user_id.hex,
        first_name="Admin first name",
        last_name="Admin last name",
        second_name="Admin second name",
        position="Admin position",
        wiki_api_client=FakeWikiApiClient(
            id=user_id,
            description="Wiki api client for Admin",
        )
    )
