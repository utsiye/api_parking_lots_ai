from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import payment as exceptions


async def payment_not_found_handler(request: Request, exc: exceptions.PaymentNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"Payment not found"},
    )
