from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.tickets import TicketDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.get('/support/{ticket_id}', status_code=200)
async def support_by_id_route(ticket_id: int, user_id: int = Depends(authorize),
                              db: DBCommands = Depends(Stub(DBCommands))) -> TicketDTO:
    ticket = await db.get_ticket(ticket_id=ticket_id, user_id=user_id)
    return ticket
