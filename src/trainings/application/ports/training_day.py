from typing import Protocol

from src.shared.application.ports import IUnitOfWork
from src.trainings.domain.training_day_model import TrainingDay


class TrainingDayRepositoryPort(Protocol):
    async def get(self, id: int) -> TrainingDay | None: ...
    async def save(self, training_day: TrainingDay) -> TrainingDay: ...


class IUnitOfWorkTrainingDay(IUnitOfWork, Protocol):
    @property
    def tr_day_repo(self) -> TrainingDayRepositoryPort: ...
