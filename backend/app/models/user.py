from app.models.base import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .month import MonthGoalModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        nullable=False,
    )

    month_goals: Mapped[list["MonthGoalModel"]] = relationship(
        "MonthGoalModel",
        back_populates="user",
    )