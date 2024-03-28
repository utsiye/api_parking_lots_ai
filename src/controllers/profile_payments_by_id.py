from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.payments import PaymentDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/profile/payments/{transaction_id}', status_code=200)
async def profile_payments_by_id_route(transaction_id: int, user_id: int = Depends(authorize),
                         db: DBCommands = Depends(Stub(DBCommands))) -> PaymentDTO:
    payment = await db.get_payment(user_id, transaction_id)
    return payment
