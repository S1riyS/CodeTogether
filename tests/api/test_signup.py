from httpx import AsyncClient

from tests.utils.random_ import random_email, random_lower_string


async def test_sucessful_signup(async_client: AsyncClient):
    signup_data = {"email": random_email(), "username": random_lower_string(), "password": random_lower_string()}
    response = await async_client.post("/api/v1/auth/signup", json=signup_data)
    print(response.json())
    assert response.status_code == 200

    content = response.json()
    assert content["email"] == signup_data["email"]
    assert content["username"] == signup_data["username"]
    assert "password" not in content
    assert content["is_verified"] == False


async def test_signup_duplicate_username(async_client: AsyncClient):
    signup_data = {"email": random_email(), "username": random_lower_string(), "password": random_lower_string()}
    response = await async_client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 200

    signup_data["email"] = random_email()
    response = await async_client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


async def test_signup_duplicate_email(async_client: AsyncClient):
    signup_data = {"email": random_email(), "username": random_lower_string(), "password": random_lower_string()}
    response = await async_client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 200

    signup_data["username"] = random_lower_string()
    response = await async_client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
