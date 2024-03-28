from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import user as exceptions


async def user_is_already_exists_handler(request: Request, exc: exceptions.UserIsAlreadyExistsException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"message": f"A user with that name is already registered."},
    )


async def user_balance_is_too_low_handler(request: Request, exc: exceptions.UserBalanceIsTooLowException) -> JSONResponse:
    return JSONResponse(
        status_code=402,
        content={"message": f"User balance is too low to process this transaction"},
    )
