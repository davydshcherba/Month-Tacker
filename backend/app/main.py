from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.postgrs import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health", status_code=200)
async def health():
    return {"status": "OK"}