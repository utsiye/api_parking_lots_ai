from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str = None
    login: str
    password: str
