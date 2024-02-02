from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from v1.app.services.db.db_models import create_db, drop_all_tables

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.pool = await create_db()

    yield

    await drop_all_tables(app.state.pool)
    await app.state.pool.close()
