from dataclasses import dataclass


@dataclass
class JWTToken:
    access_token: str
    token_type: str
    expires_in: int
