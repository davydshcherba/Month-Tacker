from enum import Enum

from app.models.base import Base
from sqlalchemy import Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ! DUO IMPORT FIX 
# from .user import UserModel

# TODO Add all month
class Month(str, Enum):
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


class MonthGoalModel(Base):
    __tablename__ = "monthgoal"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    month: Mapped[Month] = mapped_column(
        SQLEnum(Month),
        nullable=False,
    )

    user_id: Mapped["UserModel"] = relationship(back_populates="month_id")

