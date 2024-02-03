from contextlib import asynccontextmanager
from typing import AsyncGenerator
import alembic.config

from fastapi import FastAPI

from src.adapters.db.main import initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    session_maker = await initialize_db(app.state.config.db.url)
    app.state.session_maker = session_maker

    alembic.config.main(argv=[
        'upgrade', 'head',
    ])
    yield

    alembic.config.main(argv=[
        'downgrade', 'head',
    ])
