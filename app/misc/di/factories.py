from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends
import asyncpg

from app.services.db.db_commands import DBCommands
from app.misc.di.stub import Stub


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
