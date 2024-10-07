from calendar import c

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.position import create_new_position
from tests.utils.project import create_new_project
from tests.utils.user import authentication_token_from_email, create_new_user


async def test_user_can_create_position(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)

    token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=user.email,
    )
    data = {
        "name": "Test Position",
        "description": "Description of position",
        "count": 5,
    }

    response = await async_client.post(f"/api/v1/projects/{project.id}/positions", headers=token_headers, json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["count"] == data["count"]


async def test_user_can_not_create_position_for_not_authored_project(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    data = {
        "name": "Test Position",
        "description": "Description of position",
        "count": 5,
    }

    response = await async_client.post(
        f"/api/v1/projects/{project.id}/positions", headers=another_user_token_headers, json=data
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


async def test_any_user_can_retrieve_positions(async_client: AsyncClient, session: AsyncSession):
    POSITIONS_COUNT = 2

    user = await create_new_user(session)
    project = await create_new_project(session, user)

    for _ in range(POSITIONS_COUNT):
        await create_new_position(session, project)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    response = await async_client.get(f"/api/v1/projects/{project.id}/positions", headers=another_user_token_headers)
    assert response.status_code == 200

    content = response.json()
    assert len(content) == POSITIONS_COUNT

    for position in content:
        assert "name" in position
        assert "description" in position
        assert "count" in position


async def test_user_can_update_position(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)
    position = await create_new_position(session, project)

    token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=user.email,
    )
    new_data = {"name": "New Test Position", "description": "New description of position", "count": 10}
    response = await async_client.put(f"/api/v1/positions/{position.id}", headers=token_headers, json=new_data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == str(position.id)
    assert content["name"] == new_data["name"]
    assert content["description"] == new_data["description"]
    assert content["count"] == new_data["count"]


async def test_user_can_not_update_position_for_not_authored_project(
    async_client: AsyncClient,
    session: AsyncSession,
):
    project_creator = await create_new_user(session)
    project = await create_new_project(session, project_creator)
    position = await create_new_position(session, project)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    new_data = {"name": "New Test Position", "description": "New description of position", "count": 10}
    response = await async_client.put(
        f"/api/v1/positions/{position.id}",
        headers=another_user_token_headers,
        json=new_data,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


async def test_user_can_delete_position(async_client: AsyncClient, session: AsyncSession):
    user = await create_new_user(session)
    project = await create_new_project(session, user)
    position = await create_new_position(session, project)

    token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=user.email,
    )

    response = await async_client.delete(f"/api/v1/positions/{position.id}", headers=token_headers)
    assert response.status_code == 200

    response = await async_client.get(f"/api/v1/projects/{project.id}/positions", headers=token_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_user_can_not_delete_position_for_not_authored_project(async_client: AsyncClient, session: AsyncSession):
    project_creator = await create_new_user(session)
    project = await create_new_project(session, project_creator)
    position = await create_new_position(session, project)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    response = await async_client.delete(f"/api/v1/positions/{position.id}", headers=another_user_token_headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}
