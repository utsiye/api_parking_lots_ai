from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.requests import RequestDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/profile/requests/{request_id}', status_code=200)
async def profile_requests_by_id_route(request_id: int, user_id: int = Depends(authorize),
                                       db: DBCommands = Depends(Stub(DBCommands))) -> RequestDTO:
    request = await db.get_request(user_id, request_id)
    return request
