from fastapi import APIRouter

root = APIRouter(prefix="", tags=["Root"])


@root.get("/health", status_code=200)
def health():
    return {"status": "ok"}
