from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.lambdas import insp

from Backend.core.interfaces.base_repository_interfaces import (
    BaseLockRepositoryInterface,
    BaseUpdateRepositoryInterface,
)
from Backend.infrastructure.base_repository_components.base_lock_repository import (
    BaseLockRepository,
)
from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base
from Backend.utils.exceptions import DBErrorHandler


class BaseUpdateRepository[ModelT: Base, SchemaT: BaseModel, IdT: int | UUID](
    BaseRepository[ModelT], BaseUpdateRepositoryInterface[ModelT, SchemaT, IdT]
):
    def __init__(
        self,
        session: AsyncSession,
        lock_repo: BaseLockRepositoryInterface[ModelT],
        model: type[ModelT],
    ) -> None:
        self.model = model
        self.lock_repo = lock_repo
        self.pk_column = inspect(self.model).primary_key[0]
        super().__init__(session)

    async def update(self, id: IdT, data: SchemaT) -> ModelT | None:
        instance = await self.lock_repo.get_for_update(id)

        if instance is None:
            return instance

        data_dump = data.model_dump(exclude_unset=True)

        try:
            for key, value in data_dump.items():
                setattr(instance, key, value)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)

        return instance
