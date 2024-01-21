from pydantic import BaseModel
from app.services.db.dto.users import UserDTO


class User(BaseModel):
    id: str = None
    login: str
    password: str

    def to_dto(self):
        return UserDTO(
            id=self.id if self.id else '0',
            login=self.login,
            password=self.password
        )


class ShowUser(BaseModel):
    id: str
    login: str
