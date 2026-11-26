from functools import wraps
from logging import getLogger
from typing import Awaitable, Callable, Concatenate

from redis.exceptions import ConnectionError, TimeoutError

logger = getLogger(__name__)


def handle_redis_error[Self, **P, R](
    func: Callable[Concatenate[Self, P], Awaitable[R]],
) -> Callable[Concatenate[Self, P], Awaitable[R | None]]:
    @wraps(func)
    async def wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return await func(self, *args, **kwargs)
        except (ConnectionError, TimeoutError):
            logger.warning(
                "Redis is unavailable, args: %s, kwargs: %s",
                args,
                kwargs,
                exc_info=True,
            )
        return None

    return wrapper
