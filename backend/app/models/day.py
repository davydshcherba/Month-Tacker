from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class DayGoalModel(Base):
    __tablename__ = "daygoal"

    id: Mapped[int] = mapped_column(
            primary_key=True
        )

    text: Mapped[str] = mapped_column(nullable=False)

    month_id: Mapped[int] = mapped_column(
            ForeignKey("monthgoal.id"),
            nullable=False,
        )
    
    month: Mapped["MonthGoalModel"] = relationship(
            "UserModel",
            back_populates="month_goals",
        )
