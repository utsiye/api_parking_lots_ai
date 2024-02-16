from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import user as exceptions


async def user_is_already_exists_handler(request: Request, exc: exceptions.UserIsAlreadyExistsException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"message": f"A user with that name is already registered."},
    )
