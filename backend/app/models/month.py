
from app.models.base import Base
from sqlalchemy import Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.enum.month import MonthEnum

# ! DUO IMPORT FIX 
# from .user import UserModel

class MonthGoalModel(Base):
    __tablename__ = "monthgoal"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    month: Mapped[MonthEnum] = mapped_column(
        SQLEnum(MonthEnum),
        nullable=False,
    )

    user_id: Mapped["UserModel"] = relationship(back_populates="month_id")

