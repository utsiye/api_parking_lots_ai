from fastapi import Request, Depends

from src.di.stub import Stub
from src.services.security import Protector
from src.exceptions.classes.auth import UnauthorizedException


async def authorize(request: Request, protector: Protector = Depends(Stub(Protector))) -> int:
    jwt_token = request.headers.get('access-token')
    if not jwt_token:
        raise UnauthorizedException

    payload = protector.verify_token(jwt_token)

    if not payload['id']:
        raise UnauthorizedException

    return payload['id']
