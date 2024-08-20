from typing import List
from uuid import UUID

from fastapi import APIRouter

from routers.depenencies import SessionDep, CurrentUserDep
from schemas.position import PositionCreateSchema, PositionSchema
from schemas.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema
from services.position_service import PositionService
from services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectSchema)
async def create(data: ProjectCreateSchema, user: CurrentUserDep, session: SessionDep):
    project_service = ProjectService(session)
    db_obj = await project_service.create(data, user.id)
    return ProjectSchema.from_orm(db_obj)


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_one(project_id: UUID, session: SessionDep):
    project_service = ProjectService(session)
    db_obj = await project_service.get_by_id(project_id)
    return ProjectSchema.from_orm(db_obj)


@router.put("/{project_id}", response_model=ProjectSchema)
async def update(project_id: UUID, data: ProjectUpdateSchema, user: CurrentUserDep, session: SessionDep):
    project_service = ProjectService(session)
    db_obj = await project_service.update(project_id, data, user.id)
    return ProjectSchema.from_orm(db_obj)


@router.delete("/{project_id}", response_model=bool)
async def delete(project_id: UUID, user: CurrentUserDep, session: SessionDep):
    project_service = ProjectService(session)
    return await project_service.delete(project_id, user.id)


@router.post("/{project_id}/positions", response_model=PositionSchema)
async def add_position(project_id: UUID, data: PositionCreateSchema, user: CurrentUserDep, session: SessionDep):
    position_service = PositionService(session)
    db_obj = await position_service.create(project_id, data, user.id)
    return PositionSchema.from_orm(db_obj)


@router.get("/{project_id}/positions", response_model=List[PositionSchema])
async def get_positions(project_id: UUID, session: SessionDep):
    position_service = PositionService(session)
    db_list = await position_service.get_by_project_id(project_id)
    return [PositionSchema.from_orm(position) for position in db_list]
