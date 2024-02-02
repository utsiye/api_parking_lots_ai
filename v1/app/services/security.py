from datetime import timedelta, datetime
from jose import jwt

from v1.app.services.db.dto.authentication import JWTToken
from v1.app.settings.config import JWTConfig


class Protector:
    def __init__(self, config: JWTConfig):
        self.config = config

    def create_access_token(self, data: dict, life_minutes: int | None = None) -> JWTToken:
        if not life_minutes:
            life_minutes = self.config.life_duration

        to_encode = data.copy()

        expires_delta = timedelta(minutes=life_minutes)
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.encoding_algorithm)
        return JWTToken(access_token=encoded_jwt, token_type='bearer', expires_in=life_minutes*60)
