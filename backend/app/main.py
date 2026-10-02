from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.postgrs import engine
from app.models.base import Base
from backend.app.api.router import router



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title="API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(router=router, prefix="/api")