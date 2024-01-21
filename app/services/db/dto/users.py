from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: str
    login: str
    password: str
