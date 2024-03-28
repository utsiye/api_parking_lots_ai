from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes import request as exceptions


async def request_not_found_handler(request: Request, exc: exceptions.RequestNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"Request not found"},
    )
