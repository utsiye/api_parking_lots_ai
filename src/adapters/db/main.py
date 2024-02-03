from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from .models import Base
from src.misc.logger import logger


async def initialize_db(database_url: str) -> async_sessionmaker:
    logger.info("Connecting to database")

    engine = create_async_engine(database_url)

    return create_sessionmaker(engine)

def create_engine(database_url: str) -> AsyncEngine:
    logger.info("Connecting to database")

    return create_async_engine(database_url)

def create_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        autoflush=True,
        expire_on_commit=False,
    )
