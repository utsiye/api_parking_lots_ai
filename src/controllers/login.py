from fastapi import APIRouter, Depends, HTTPException, status

from src.di.stub import Stub
from src.adapters.db.db_commands import DBCommands
from src.misc.dto.authentication import JWTToken
from src.misc.dto.users import UserDTO, UserInput
from src.adapters.security import Protector

api_router = APIRouter()


@api_router.post('/login', status_code=200, response_model=JWTToken)
async def login_route(user: UserInput, protector: Protector = Depends(Stub(Protector)),
                         db: DBCommands = Depends(Stub(DBCommands))) -> JWTToken:
    user_dto = UserDTO(id=None, login=user.login, password=user.password)
    auth_user = await db.authenticate_user(user_dto)

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    jwt_token = protector.create_access_token(data={"sub": user.login})
    return jwt_token
