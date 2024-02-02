from dataclasses import dataclass


@dataclass
class UserDTO:
    id: str
    login: str
    password: str

@dataclass
class UserInput:
    login: str
    password: str

@dataclass
class UserOutput:
    id: str
    login: str

