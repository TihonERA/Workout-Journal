import pytest
from faker import Faker

from src.tests.unit.fake_objects.fake_unit_of_work import FakeUnitOfWork
from src.tests.unit.trainings.factories.workout_factories import WorkoutDTOFactory
from src.tests.unit.trainings.fake_objects.fake_workout_reader import FakeWorkoutReader
from src.trainings.application.use_cases.workout.create_workout import (
    CreateWorkoutUseCase,
)
from src.trainings.application.use_cases.workout.delete_workout import (
    DeleteWorkoutUseCase,
)
from src.trainings.application.use_cases.workout.get_workout import GetWorkoutUseCase
from src.trainings.application.use_cases.workout.update_workout import (
    UpdateWorkoutUseCase,
)


@pytest.fixture
def create_workout_use_case(fake_uow: FakeUnitOfWork) -> CreateWorkoutUseCase:
    return CreateWorkoutUseCase(fake_uow)


@pytest.fixture
def delete_workout_use_case(fake_uow: FakeUnitOfWork) -> DeleteWorkoutUseCase:
    return DeleteWorkoutUseCase(fake_uow)


@pytest.fixture
def get_workout_use_case(workout_reader: FakeWorkoutReader) -> GetWorkoutUseCase:
    return GetWorkoutUseCase(workout_reader)


@pytest.fixture
def update_workout_use_case(fake_uow: FakeUnitOfWork) -> UpdateWorkoutUseCase:
    return UpdateWorkoutUseCase(fake_uow)


@pytest.fixture
def workout_dto_factory(faker: Faker) -> WorkoutDTOFactory:
    return WorkoutDTOFactory(faker)
