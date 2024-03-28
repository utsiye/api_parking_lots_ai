from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.payments import PaymentDTO
from src.misc.dto.common import PaginationDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/profile/payments', status_code=200)
async def profile_payments_route(skip: int = 0, limit: int = 100, user_id: int = Depends(authorize),
                                 db: DBCommands = Depends(Stub(DBCommands))) -> list[PaymentDTO]:
    pagination = PaginationDTO(skip=skip, limit=limit)
    payments = await db.get_all_user_payments(user_id, pagination)
    return payments
