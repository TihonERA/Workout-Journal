from redis.asyncio import ConnectionPool, Redis

from src.core.config import get_settings

redis_pool = ConnectionPool.from_url(
    url=str(get_settings().REDIS_URL), max_connection=20
)

redis_client = Redis(connection_pool=redis_pool)
