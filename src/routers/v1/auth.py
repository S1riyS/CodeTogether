from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from routers.depenencies import SessionDep
from schemas.auth import TokenSchema
from schemas.user import UserSchema, UserCreateSchema as SignUpSchema
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema)
async def login(session: SessionDep, data: OAuth2PasswordRequestForm = Depends()):
    auth_service = AuthService(session)
    return await auth_service.login(data)


@router.post("/signup", response_model=UserSchema)
async def signup(data: SignUpSchema, session: SessionDep):
    auth_service = AuthService(session)
    db_obj = await auth_service.signup(data)
    return UserSchema.from_orm(db_obj)
