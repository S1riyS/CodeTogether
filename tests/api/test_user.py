from typing import Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.typing_ import UserCredentials
from tests.utils.user import authentication_token_from_email, create_new_user


async def test_get_me(
    async_client: AsyncClient, default_user_token_headers: Dict[str, str], defalt_user_credentials: UserCredentials
):
    response = await async_client.get("/api/v1/users/me", headers=default_user_token_headers)
    assert response.status_code == 200

    content = response.json()
    assert content["email"] == defalt_user_credentials.email
    assert content["username"] == defalt_user_credentials.username


async def test_update_me(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)

    new_username = "new_username"
    response = await async_client.put("/api/v1/users/me", headers=token_headers, json={"username": new_username})
    assert response.status_code == 200

    content = response.json()
    assert content["username"] == new_username
