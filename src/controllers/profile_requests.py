from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.requests import RequestDTO
from src.misc.dto.common import PaginationDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/profile/requests', status_code=200)
async def profile_requests_route(skip: int = 0, limit: int = 100, user_id: int = Depends(authorize),
                                 db: DBCommands = Depends(Stub(DBCommands))) -> list[RequestDTO]:
    pagination = PaginationDTO(skip=skip, limit=limit)
    requests = await db.get_all_user_requests(user_id, pagination)
    return requests
