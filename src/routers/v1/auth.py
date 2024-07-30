from fastapi import APIRouter

from routers.depenencies import SessionDep
from schemas.auth import TokenSchema, LoginSchema
from schemas.user import UserSchema, UserCreateSchema as SignupSchema
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema)
async def login(data: LoginSchema, session: SessionDep):
    auth_service = AuthService(session)
    return await auth_service.login(data)


@router.post("/signup", response_model=UserSchema)
async def signup(data: SignupSchema, session: SessionDep):
    auth_service = AuthService(session)
    db_obj = await auth_service.signup(data)
    return UserSchema.from_orm(db_obj)
