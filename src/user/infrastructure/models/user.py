from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from Backend.models.base import Base
from sqlalchemy import String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .exercise_history import ExerciseHistory
    from .workout import Workout

class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )
    login: Mapped[str] = mapped_column(
        String(32),
        index=True,
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False
    )
    hash_password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    workouts: Mapped[list["Workout"]] = relationship(back_populates="user")
    exercises_history: Mapped[list["ExerciseHistory"]] = relationship(back_populates="user")
