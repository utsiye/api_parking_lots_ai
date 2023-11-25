from typing import Annotated

from fastapi import APIRouter, Depends

from app.misc.di.stub import Stub
from app.services.db.db_commands import DBCommands
from app.misc.models.user import User

api_router = APIRouter()


@api_router.post('/register')
async def register_route(user: User, db: Annotated[DBCommands, Depends(Stub(DBCommands))]) -> dict:
    user = await db.get_or_create_user(login=user.login, password=user.password)
    return user.to_dict()
