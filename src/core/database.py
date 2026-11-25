from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import get_settings

async_engine = create_async_engine(url=str(get_settings().POSTGRES_URL), echo=False)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
