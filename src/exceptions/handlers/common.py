from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.classes.common import MissingRequiredParameterException


async def missing_required_parameter_handler(request: Request, exc: MissingRequiredParameterException) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": f"Not enough parameters to process the request"}
    )
