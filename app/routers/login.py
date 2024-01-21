from fastapi import APIRouter, Depends, HTTPException, status

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.misc.models.authentication import JWTToken, authForm
from app.services.security import Protector

api_router = APIRouter()


@api_router.post('/login', status_code=200, response_model=JWTToken)
async def register_route(auth_data: authForm,
                         protector: Protector = Depends(Stub(Protector)),
                         db: DBCommands = Depends(Stub(DBCommands))) -> JWTToken:
    user = await db.authenticate_user(auth_data.login, auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    jwt_token = protector.create_access_token(data={"sub": user.login})
    print(jwt_token)
    return jwt_token
