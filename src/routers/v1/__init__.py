from fastapi import APIRouter

from . import application, auth, position, project, user

router = APIRouter(prefix="/v1")


router.include_router(auth.router)
router.include_router(user.router)
router.include_router(project.router)
router.include_router(position.router)
router.include_router(application.router)
