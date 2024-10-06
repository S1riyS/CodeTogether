from fastapi import APIRouter

from routers import root, v1

router = APIRouter(prefix="/api")

router.include_router(root)
router.include_router(v1.router)
