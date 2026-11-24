from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=False)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
