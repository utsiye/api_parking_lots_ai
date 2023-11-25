import asyncpg
from fastapi import FastAPI

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.misc.di.factories import di_db_gateway_factory, di_connection_factory

def setup_di(app: FastAPI):
    app.dependency_overrides[Stub(asyncpg.Pool)] = lambda: app.state.pool
    app.dependency_overrides[Stub(asyncpg.Connection)] = di_connection_factory
    app.dependency_overrides[Stub(DBCommands)] = di_db_gateway_factory
