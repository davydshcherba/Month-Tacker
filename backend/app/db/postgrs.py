from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import settings
from app.models.base import Base

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
    f"/{settings.DB_NAME}"
)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session