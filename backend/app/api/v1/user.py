from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import UserModel
from app.db.postgrs import get_db
from app.utils.hasher import Hasher
from app.schemas.user import UserRegister, UserLogin
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

@user_router.post("/login")
async def login(
    data: UserLogin,
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(
        select(UserModel).where(
            UserModel.username == data.username
        )
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    if not Hasher.verify_password(data.password, user.hashed_password):
        return "Invalid data"

    token = encode_access_JWT({"user_id": user.id})

    return {"access_token": token}