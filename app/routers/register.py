from fastapi import APIRouter, Depends

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.misc.models.user import User, ShowUser
from app.services.db.dto.users import UserDTO

api_router = APIRouter()


@api_router.post('/register', status_code=201, response_model=ShowUser)
async def register_route(user: User, db: DBCommands = Depends(Stub(DBCommands))) -> UserDTO:
    user = await db.get_or_create_user(login=user.login, password=user.password)
    return ShowUser(id=user.id, login=user.login) # TODO обработка ошибок
