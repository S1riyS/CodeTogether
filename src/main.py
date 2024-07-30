from fastapi import FastAPI

from routers.api import router

app = FastAPI()

app.include_router(router)
