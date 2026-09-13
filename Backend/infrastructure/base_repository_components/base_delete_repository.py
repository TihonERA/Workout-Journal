from uuid import UUID

from sqlalchemy import delete, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.core.interfaces.base_repository_interfaces import (
    BaseDeleteRepositoryInterface,
    BaseLockRepositoryInterface,
)
from Backend.infrastructure.base_repository_components.base_repository import (
    BaseRepository,
)
from Backend.models.base import Base
from Backend.utils.exceptions import DBErrorHandler


class BaseDeleteRepository[ModelT: Base, IdT: int | UUID](
    BaseRepository[ModelT], BaseDeleteRepositoryInterface[ModelT, IdT]
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

    async def delete(self, id: IdT) -> bool:
        instance = await self.lock_repo.get_for_update(id)

        if instance is None:
            return False

        try:
            await self.session.delete(instance)
            await self.flush()
        except IntegrityError as e:
            DBErrorHandler.handle_integrity_error(e)

        return True
