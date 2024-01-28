from fastapi import APIRouter, Depends

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.services.db.dto.users import UserDTO, UserInput, UserOutput
from app.services.db.dto.payment import PaymentInput

api_router = APIRouter()


@api_router.post('/top-up/', status_code=201, response_model=...)
async def register_route(payment: ..., db: DBCommands = Depends(Stub(DBCommands))) -> UserDTO:
    ...
    return ...
