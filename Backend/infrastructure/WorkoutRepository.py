from pydantic.main import ModelT

from Backend.core.interfaces.base_repository_interfaces import (
    BaseCreateRepositoryInterface,
    BaseDeleteRepositoryInterface,
    BaseReadRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.infrastructure.base_repository_components.base_create_repository import (
    BaseCreateRepository,
)
from Backend.infrastructure.base_repository_components.base_delete_repository import (
    BaseDeleteRepository,
)
from Backend.infrastructure.base_repository_components.base_update_repository import (
    BaseUpdateRepository,
)
from Backend.schemas.workout import (
    WorkoutCreateDTO,
    WorkoutGetAllFilterDTO,
    WorkoutUpdate,
)
from Backend.services.workout.interfaces import WorkoutRepositoryInterface
from Backend.infrastructure.base_repository_components.base_read_repository import (
    BaseReadRepository,
)
from Backend.models.workout import Workout
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy import and_, select
from Backend.models.trainingday import TrainingDay
from Backend.models.dayexercise import DayExercise
from Backend.models.muscle import Muscle
from Backend.models.exercise import Exercise
from Backend.models.muscle_antagonists import MuscleAntagonists
from typing import Sequence, Any, final
from uuid import UUID


@final
class WorkoutRepository(WorkoutRepositoryInterface, BaseRepository[Workout]):

    def __init__(
        self,
        session: AsyncSession,
        create_repo: BaseCreateRepositoryInterface[Workout, WorkoutCreateDTO],
        read_repo: BaseReadRepositoryInterface[Workout],
        update_repo: BaseUpdateRepositoryInterface[Workout, WorkoutUpdate, int],
        delete_repo: BaseDeleteRepositoryInterface[Workout, int],
    ):
        self.create_repo = create_repo
        self.read_repo = read_repo
        self.update_repo = update_repo
        self.delete_repo = delete_repo

    async def create(self, data: WorkoutCreateDTO) -> Workout:
        return await self.create_repo.create(data)

    async def get_loaded(self, id: int) -> Workout | None:
        return await self.read_repo._get_instance_by_column(
            column=Workout.id,
            search_value=id,
            options=[
                selectinload(Workout.training_days).selectinload(
                    TrainingDay.day_exercises
                )
            ],
        )

    async def get_all(self, data: WorkoutGetAllFilterDTO) -> Sequence[Workout]:
        stmt = select(Workout)
        if data.target_user_id:
            stmt = stmt.where(
                Workout.user_id == data.target_user_id,
            )
        if data.public:
            stmt = stmt.where(Workout.public == data.public)
        stmt = stmt.offset(data.skip).limit(data.limit)

        result = await self.execute(stmt)
        return result.scalars().all()

    async def update(self, id: int, data: WorkoutUpdate) -> Workout | None:
        return await self.update_repo.update(id, data)

    async def delete(self, id: int) -> bool:
        return await self.delete_repo.delete(id)
