from fastapi import APIRouter

from routers.v1 import user, auth

router = APIRouter(prefix="/api/v1")

router.include_router(user.router)
router.include_router(auth.router)