from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.db.postgrs import get_db
from app.utils.hasher import Hasher
from app.schemas.user import UserRegister
from app.utils.JWT import encode_access_JWT
user_router = APIRouter()

@user_router.post("/register")
async def register(
    data: UserRegister,
    session: AsyncSession = Depends(get_db),
):
    hashed_password = Hasher.get_password_hash(data.password)
    user = UserModel(
        username=data.username,
        name=data.name,
        hashed_password=hashed_password
    )
    session.add(user)

    await session.commit()
    await session.refresh(user)

    token = encode_access_JWT({
        "user_id": user.id
    })
    return token