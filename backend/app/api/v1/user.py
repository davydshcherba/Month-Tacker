from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.db.postgrs import get_db

user_router = APIRouter()

@user_router.post("/register")
async def register(
    session: AsyncSession = Depends(get_db)
):
    user = UserModel(
        username="davyd",
        name="Davyd",
        hashed_password="test_password"
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user