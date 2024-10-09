from httpx import AsyncClient


async def test_health(async_client: AsyncClient):
    response = await async_client.get("/api/health")
    assert response.status_code == 200

    content = response.json()
    assert content["status"] == "ok"
