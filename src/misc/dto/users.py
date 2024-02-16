from typing import Optional

from dataclasses import dataclass


@dataclass
class UserDTO:
    login: Optional[str] = None
    password: Optional[str] = None
    balance: Optional[int] = None
    id: Optional[int] = None

@dataclass
class UserInput:
    login: str
    password: str

@dataclass
class UserOutput:
    id: int
    login: str

@dataclass
class ProfileOutput:
    id: int
    login: str
    balance: int

@dataclass
class UpdateUserInput:
    new_password: str

