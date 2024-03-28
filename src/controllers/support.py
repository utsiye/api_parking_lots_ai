from fastapi import APIRouter, Depends

from src.di.stub import Stub
from src.services.db.db_commands import DBCommands
from src.misc.dto.tickets import MessageInput, CreateTicketDTO, TicketDTO
from src.di.auth import authorize

api_router = APIRouter()


@api_router.post('/support', status_code=201)
async def create_support_route(message: MessageInput, user_id: int = Depends(authorize),
                               db: DBCommands = Depends(Stub(DBCommands))) -> TicketDTO:
    ticket_dto = CreateTicketDTO(user_id=user_id, text=message.description)
    ticket = await db.create_ticket(ticket_dto)
    return ticket


@api_router.put('/support/{ticket_id}', status_code=200)
async def add_message_support_route(ticket_id: int, message: MessageInput, user_id: int = Depends(authorize),
                                    db: DBCommands = Depends(Stub(DBCommands))) -> TicketDTO:
    ticket = await db.add_ticket_message(ticket_id=ticket_id, text=message.description)
    return ticket
