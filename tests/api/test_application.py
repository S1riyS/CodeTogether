import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.associations.application import ApplicationStatus
from schemas import application
from tests.utils.application import create_new_application, set_status
from tests.utils.position import create_new_position
from tests.utils.project import create_new_project
from tests.utils.random_ import random_uuid
from tests.utils.user import authentication_token_from_email, create_new_user


async def test_user_can_apply(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    applicant = await create_new_user(session)
    applicant_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=applicant.email,
    )

    data = {"message": "I want to apply for this position"}

    response = await async_client.post(
        f"/api/v1/positions/{position.id}/applications",
        headers=applicant_token_headers,
        json=data,
    )
    assert response.status_code == 200
    assert response.json()["message"] == data["message"]


async def test_user_can_not_apply_when_there_are_no_vacant_slots(async_client: AsyncClient, session: AsyncSession):
    VACANT_SLOTS = 2

    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project, count=VACANT_SLOTS)

    for _ in range(VACANT_SLOTS):
        # All "previous" applications are "already approved"
        application = await create_new_application(session, position)
        await set_status(session, application, ApplicationStatus.APPROVED)

    another_applicant = await create_new_user(session)
    another_applicant_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_applicant.email,
    )

    data = {"message": "I want to apply for this position"}
    response = await async_client.post(
        f"/api/v1/positions/{position.id}/applications",
        headers=another_applicant_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "There are no vacant slots for this position"}


async def test_user_can_not_apply_if_he_is_the_project_owner(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    project_owner_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=project_owner.email,
    )

    data = {"message": "I want to apply for this position"}
    response = await async_client.post(
        f"/api/v1/positions/{position.id}/applications",
        headers=project_owner_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The owner cannot apply for positions in his project"}


@pytest.mark.parametrize(
    "status",
    (
        ApplicationStatus.APPROVED,
        ApplicationStatus.REJECTED,
    ),
)
async def test_user_can_set_status_for_application(
    async_client: AsyncClient,
    session: AsyncSession,
    status: ApplicationStatus,
):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    application = await create_new_application(session, position)

    project_owner_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=project_owner.email,
    )

    methods_mapping = {
        ApplicationStatus.APPROVED: "approved",
        ApplicationStatus.REJECTED: "rejected",
    }

    response = await async_client.post(
        f"/api/v1/applications/{application.id}/{methods_mapping[status]}",
        headers=project_owner_token_headers,
    )
    assert response.status_code == 200


async def test_user_can_not_approve_when_there_are_no_vacant_slots(async_client: AsyncClient, session: AsyncSession):
    VACANT_SLOTS = 2
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project, count=VACANT_SLOTS)

    other_applications = []
    for _ in range(VACANT_SLOTS):
        current_application = await create_new_application(session, position)
        other_applications.append(current_application)

    # Create another applicant which will not be able to be approved
    another_applicant = await create_new_user(session)
    current_application = await create_new_application(session, position, another_applicant)
    another_applicant_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_applicant.email,
    )

    # Approve all applications exect one from "another applicant"
    for i in range(VACANT_SLOTS):
        await set_status(session, other_applications[i], ApplicationStatus.APPROVED)

    # Try to approve another application
    response = await async_client.post(
        f"/api/v1/applications/{current_application.id}/approved",
        headers=another_applicant_token_headers,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "There are no vacant slots for this position"}


async def test_user_can_retrieve_applications(
    async_client: AsyncClient,
    session: AsyncSession,
):
    APPLICATIONS_COUNT = 3

    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    for _ in range(APPLICATIONS_COUNT):
        await create_new_application(session, position)

    owner_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=project_owner.email,
    )
    response = await async_client.get(f"/api/v1/positions/{position.id}/applications", headers=owner_token_headers)
    assert response.status_code == 200
    assert len(response.json()) == APPLICATIONS_COUNT


async def test_user_can_not_retrieve_application_for_not_exist_position(
    async_client: AsyncClient,
    session: AsyncSession,
):
    user = await create_new_user(session)
    token_headers = await authentication_token_from_email(async_client=async_client, session=session, email=user.email)

    not_exisiting_id = random_uuid()
    response = await async_client.get(f"/api/v1/positions/{not_exisiting_id}/applications", headers=token_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Position not found"}


async def test_user_can_not_retrieve_application_for_not_authored_position(
    async_client: AsyncClient,
    session: AsyncSession,
):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    response = await async_client.get(
        f"/api/v1/positions/{position.id}/applications",
        headers=another_user_token_headers,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


async def test_user_can_update_application_if_he_owns_it(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    applicant = await create_new_user(session)
    application = await create_new_application(session, position, applicant)

    applicant_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=applicant.email,
    )

    new_data = {"message": "New message from applicant"}
    response = await async_client.put(
        f"/api/v1/applications/{application.id}",
        headers=applicant_token_headers,
        json=new_data,
    )
    assert response.status_code == 200

    content = response.json()
    assert content["message"] == new_data["message"]


async def test_user_can_not_update_application_if_he_does_not_own_it(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    applicant = await create_new_user(session)
    application = await create_new_application(session, position, applicant)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    new_data = {"message": "New message from applicant"}
    response = await async_client.put(
        f"/api/v1/applications/{application.id}",
        headers=another_user_token_headers,
        json=new_data,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


async def test_user_can_delete_application_if_he_owns_it(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    applicant = await create_new_user(session)
    application = await create_new_application(session, position, applicant)

    applicant_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=applicant.email,
    )

    response = await async_client.delete(f"/api/v1/applications/{application.id}", headers=applicant_token_headers)
    assert response.status_code == 200

    project_owner_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=project_owner.email,
    )

    response = await async_client.get(
        f"/api/v1/positions/{position.id}/applications",
        headers=project_owner_token_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_user_can_not_delete_application_if_he_does_not_own_it(async_client: AsyncClient, session: AsyncSession):
    project_owner = await create_new_user(session)
    project = await create_new_project(session, project_owner)
    position = await create_new_position(session, project)

    applicant = await create_new_user(session)
    application = await create_new_application(session, position, applicant)

    another_user = await create_new_user(session)
    another_user_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=another_user.email,
    )

    response = await async_client.delete(f"/api/v1/applications/{application.id}", headers=another_user_token_headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}

    project_owner_token_headers = await authentication_token_from_email(
        async_client=async_client,
        session=session,
        email=project_owner.email,
    )

    response = await async_client.get(
        f"/api/v1/positions/{position.id}/applications",
        headers=project_owner_token_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
