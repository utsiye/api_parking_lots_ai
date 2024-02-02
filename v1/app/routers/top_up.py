from fastapi import APIRouter, Depends

from v1.app.misc.di.stub import Stub
from v1.app.services.db.db_commands import DBCommands
from v1.app.services.db.dto.users import UserDTO

api_router = APIRouter()


@api_router.post('/top-up/', status_code=201, response_model=...)
async def register_route(payment: ..., db: DBCommands = Depends(Stub(DBCommands))) -> UserDTO:
    ...
    return ...
