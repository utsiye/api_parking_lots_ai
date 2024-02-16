from contextlib import asynccontextmanager
from typing import AsyncGenerator
import subprocess

from fastapi import FastAPI

from src.services.db.main import initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    session_maker = await initialize_db(app.state.config.db.url)
    app.state.session_maker = session_maker

    subprocess.run(['alembic', 'downgrade', 'head'])
    subprocess.run(['alembic', 'upgrade', 'head'])
    yield
