from fastapi import APIRouter, Depends, HTTPException, status

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.services.db.dto.authentication import JWTToken
from app.services.db.dto.users import UserInput, UserDTO
from app.services.security import Protector

api_router = APIRouter()


@api_router.post('/login', status_code=200, response_model=JWTToken)
async def register_route(user: UserInput, protector: Protector = Depends(Stub(Protector)),
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
