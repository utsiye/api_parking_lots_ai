from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.users import UserDTO, UserInput, UserOutput

api_router = APIRouter()


@api_router.post('/register', status_code=201)
async def register_route(user: UserInput, db: DBCommands = Depends(Stub(DBCommands))) -> UserOutput:
    user_dto = UserDTO(login=user.login, password=user.password)
    user = await db.get_or_create_user(user_dto)
    return UserOutput(id=user.id, login=user.login)
