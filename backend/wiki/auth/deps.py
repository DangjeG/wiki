from fastapi import Security

from wiki.auth.core import WikiBearer

bearer_token = WikiBearer(auto_error=False)


async def get_user(token: str = Security(bearer_token)):
    pass
