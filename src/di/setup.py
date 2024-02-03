from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import FastAPI

from .stub import Stub
from src.adapters.db.db_commands import DBCommands
from src.adapters.security import Protector
from .factories import di_db_gateway_factory, di_connection_factory, di_protector_factory
from src.settings.config import Config

def setup_di(app: FastAPI, config: Config):
    app.dependency_overrides[Stub(async_sessionmaker)] = lambda: app.state.session_maker
    app.dependency_overrides[Stub(AsyncSession)] = di_connection_factory
    app.dependency_overrides[Stub(DBCommands)] = di_db_gateway_factory
    app.dependency_overrides[Stub(Protector)] = di_protector_factory
    app.dependency_overrides[Stub(Config)] = lambda: config
