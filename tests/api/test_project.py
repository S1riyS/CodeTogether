from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.project import create_new_project
from tests.utils.random_ import random_uuid
from tests.utils.user import authentication_token_from_email, create_new_user


async def test_user_can_not_retrieve_not_exist_project(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)

    not_exisiting_id = random_uuid()
    response = await async_client.get(f"/api/v1/projects/{not_exisiting_id}", headers=token_headers)
    assert response.status_code == 404


async def test_user_can_create_project(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)

    data = {"name": "Test Project", "description": "Description of project", "difficulty": "easy"}
    response = await async_client.post("/api/v1/projects/", headers=token_headers, json=data)
    assert response.status_code == 200

    content = response.json()
    project_id = content["id"]

    response = await async_client.get(f"/api/v1/projects/{project_id}", headers=token_headers)
    assert response.status_code == 200

    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["difficulty"] == data["difficulty"]
    assert content["owner_id"] == str(user.id)


async def test_user_can_update_project(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)

    new_data = {"name": "New Test Project", "description": "New description of project", "difficulty": "medium"}
    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)
    response = await async_client.put(f"/api/v1/projects/{project.id}", headers=token_headers, json=new_data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == str(project.id)
    assert content["name"] == new_data["name"]
    assert content["description"] == new_data["description"]
    assert content["difficulty"] == new_data["difficulty"]
    assert content["owner_id"] == str(user.id)


async def test_user_can_not_update_project_that_is_not_authored_by_him(
    async_client: AsyncClient,
    session: AsyncSession,
):
    project_creator = await create_new_user(session)
    project = await create_new_project(session, project_creator)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    new_data = {"name": "New Test Project", "description": "New description of project", "difficulty": "medium"}
    response = await async_client.put(
        f"/api/v1/projects/{project.id}",
        headers=another_user_token_headers,
        json=new_data,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


async def test_user_can_delete_project(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)

    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)
    response = await async_client.delete(f"/api/v1/projects/{project.id}", headers=token_headers)
    assert response.status_code == 200

    response = await async_client.get(f"/api/v1/projects/{project.id}", headers=token_headers)
    assert response.status_code == 404


async def test_user_can_not_delete_project_that_is_not_authored_by_him(
    async_client: AsyncClient,
    session: AsyncSession,
):
    project_creator = await create_new_user(session)
    project = await create_new_project(session, project_creator)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    response = await async_client.delete(
        f"/api/v1/projects/{project.id}",
        headers=another_user_token_headers,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}
