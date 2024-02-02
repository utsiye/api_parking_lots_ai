from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends
import asyncpg

from v1.app.services.db.db_commands import DBCommands
from v1.app.misc.di.stub import Stub
from v1.app.services.security import Protector
from v1.app.settings.config import Config


@asynccontextmanager
async def connection_factory(pool: asyncpg.Pool) -> AsyncGenerator[asyncpg.pool.PoolConnectionProxy, None]:
    async with pool.acquire() as connection:
        yield connection


async def di_connection_factory(pool: Annotated[asyncpg.Pool, Depends(Stub(asyncpg.Pool))]
                                ) -> AsyncGenerator[asyncpg.pool.PoolConnectionProxy, None]:
    async with connection_factory(pool=pool) as connection:
        yield connection


def di_db_gateway_factory(connection: Annotated[asyncpg.Connection, Depends(Stub(asyncpg.Connection))]) -> DBCommands:
    return DBCommands(conn=connection)


def di_protector_factory(conf: Annotated[Config, Depends(Stub(Config))]) -> Protector:
    return Protector(config=conf.jwt)
