from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.db.postgrs import get_db
from app.utils.hasher import Hasher
user_router = APIRouter()

@user_router.post("/register")
async def register(
    username: str,
    name: str,
    password: str,
    session: AsyncSession = Depends(get_db),
):
    hashed_password = Hasher.get_password_hash(password)
    print(hashed_password)
    user = UserModel(
        username=username,
        name=name,
        hashed_password=hashed_password
    )
    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user