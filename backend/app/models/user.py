from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )   

    name: Mapped[str] = mapped_column(
            String(50),
            unique=True,
            nullable=False,
        ) 

    hashed_password: Mapped[str] = mapped_column(
            String(50),
            unique=True,
            nullable=False,
        ) 
    
