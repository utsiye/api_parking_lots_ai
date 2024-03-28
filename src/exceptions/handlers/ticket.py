from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import ticket as exceptions


async def ticket_not_found_handler(request: Request, exc: exceptions.TicketNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"Ticket not found"},
    )
