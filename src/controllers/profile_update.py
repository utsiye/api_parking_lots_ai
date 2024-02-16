from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.users import UpdateUserInput, ProfileOutput, UserDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.put('/profile/update', status_code=200, response_model=ProfileOutput)
async def register_route(user: UpdateUserInput,
                         user_id: int = Depends(authorize),
                         db: DBCommands = Depends(Stub(DBCommands))) -> ProfileOutput:
    user = await db.update_user_password(user_id, user.new_password)
    return ProfileOutput(id=user.id, login=user.login, balance=user.balance)
