from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import auth as exceptions


async def unauthorized_handler(request: Request, exc: exceptions.UnauthorizedException) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": f"Incorrect login or password"},
    )

async def token_expired_handler(request: Request, exc: exceptions.TokenExpiredException) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": f"JWT-Token has expired"},
    )

async def token_invalid_handler(request: Request, exc: exceptions.TokenInvalidException) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"message": f"JWT-Token is invalid"},
    )
