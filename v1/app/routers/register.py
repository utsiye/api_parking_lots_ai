from fastapi import APIRouter, Depends

from v1.app.misc.di.stub import Stub
from v1.app.services.db.db_commands import DBCommands
from v1.app.services.db.dto.users import UserDTO, UserInput, UserOutput

api_router = APIRouter()


@api_router.post('/register', status_code=201, response_model=UserOutput)
async def register_route(user: UserInput, db: DBCommands = Depends(Stub(DBCommands))) -> UserOutput:
    user_dto = UserDTO(id=None, login=user.login, password=user.password)
    user = await db.get_or_create_user(user_dto)
    return UserOutput(id=user.id, login=user.login)
