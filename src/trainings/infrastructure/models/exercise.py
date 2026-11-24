from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from Backend.shared.infrastructure.base import Base


class TypeOfExercises(Enum):
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    STABILITY = "stability"


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[TypeOfExercises] = mapped_column(
        Enum(TypeOfExercises, name="type_of_exercises", nullable=False)
    )
