from fastapi import APIRouter, Depends, HTTPException, status

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.authentication import JWTToken
from src.misc.dto.users import UserDTO, UserInput
from src.services.security import Protector

from src.exceptions.classes.auth import UnauthorizedException

api_router = APIRouter()


@api_router.post('/login', status_code=200)
async def login_route(user: UserInput, protector: Protector = Depends(Stub(Protector)),
                      db: DBCommands = Depends(Stub(DBCommands))) -> JWTToken:
    user_dto = UserDTO(login=user.login, password=user.password)
    auth_user = await db.authenticate_user(user_dto)
    if not auth_user:
        raise UnauthorizedException

    jwt_token = protector.create_access_token(data={"id": auth_user.id})

    return jwt_token
