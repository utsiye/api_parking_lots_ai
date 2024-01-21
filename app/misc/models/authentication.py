from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class authForm(BaseModel):
    login: str
    password: str
