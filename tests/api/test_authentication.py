from httpx import AsyncClient


async def test_no_jwt_token(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


async def test_invalid_jwt_token(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users/me", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
