from typing import Self


class FakeUnitOfWork:
    def __init__(self, tr_day_repo=None, workout_repo=None) -> None:
        self.tr_day_repo = tr_day_repo
        self.workout_repo = workout_repo
        self.committed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
