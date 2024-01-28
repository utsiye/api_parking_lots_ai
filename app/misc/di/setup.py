import asyncpg
from fastapi import FastAPI

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.services.security import Protector
from app.misc.di.factories import di_db_gateway_factory, di_connection_factory, di_protector_factory
from app.settings.config import Config

def setup_di(app: FastAPI, config: Config):
    app.dependency_overrides[Stub(asyncpg.Pool)] = lambda: app.state.pool
    app.dependency_overrides[Stub(asyncpg.Connection)] = di_connection_factory
    app.dependency_overrides[Stub(DBCommands)] = di_db_gateway_factory
    app.dependency_overrides[Stub(Protector)] = di_protector_factory
    app.dependency_overrides[Stub(Config)] = lambda: config
