from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastapi import Depends

from src.adapters.db.db_commands import DBCommands
from src.di.stub import Stub
from src.adapters.security import Protector
from src.settings.config import Config


async def di_connection_factory(pool: Annotated[async_sessionmaker, Depends(Stub(async_sessionmaker))]) -> AsyncSession:
    async with pool() as connection:
        yield connection

def di_db_gateway_factory(connection: Annotated[AsyncSession, Depends(Stub(AsyncSession))]) -> DBCommands:
    return DBCommands(conn=connection)


def di_protector_factory(conf: Annotated[Config, Depends(Stub(Config))]) -> Protector:
    return Protector(config=conf.jwt)
