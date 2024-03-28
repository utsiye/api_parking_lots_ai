from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.users import ProfileOutput, UserDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/profile', status_code=200)
async def profile_route(user_id: int = Depends(authorize), db: DBCommands = Depends(Stub(DBCommands))) -> ProfileOutput:
    user_dto = UserDTO(id=user_id)
    user = await db.get_or_create_user(user_dto)
    return ProfileOutput(id=user.id, login=user.login, balance=user.balance)
