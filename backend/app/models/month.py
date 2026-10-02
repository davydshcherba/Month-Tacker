from app.models.base import Base
from app.utils.enum.month import MonthEnum

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MonthGoalModel(Base):
    __tablename__ = "monthgoal"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    text: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    month: Mapped[MonthEnum] = mapped_column(
        SQLEnum(
            MonthEnum,
            name="monthenum",
            create_type=True,
        ),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="month_goals",
    )