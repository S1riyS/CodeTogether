from httpx import AsyncClient

from tests.typing_ import UserCredentials


async def test_successful_login(async_client: AsyncClient, defalt_user_credentials: UserCredentials):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": defalt_user_credentials.email, "password": defalt_user_credentials.password},
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert "token_type" in content


async def test_wrong_credentials_login(async_client: AsyncClient, defalt_user_credentials: UserCredentials):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": defalt_user_credentials.email, "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
