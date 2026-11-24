from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backend.shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .dayexercise import DayExerciseModel
    from .workout import WorkoutModel


class TrainingDayModel(Base):
    __tablename__ = "trainingday"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    day_order: Mapped[int] = mapped_column(nullable=False)

    workout: Mapped["WorkoutModel"] = relationship(
        back_populates="training_days",
    )
    day_exercises: Mapped[list["DayExerciseModel"]] = relationship(
        back_populates="training_day", cascade="all, delete-orphan"
    )
    __table_args__ = (
        UniqueConstraint("workout_id", "day_order", name="uq_workout_day_order"),
    )
