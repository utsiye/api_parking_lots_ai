from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.di.auth import authorize

api_router = APIRouter()


@api_router.post('/top-up', status_code=201)
async def top_up_route(user_id: int = Depends(authorize),
                       db: DBCommands = Depends(Stub(DBCommands))) -> ...:
    pass

