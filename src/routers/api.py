from fastapi import APIRouter

from routers.v1 import user, auth, project, health

router = APIRouter(prefix="/api/v1")


router.include_router(health.router)
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(project.router)
