from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: str
    login: str
    password: str

    def to_dict(self):
        return {'id': self.id,
                'login': self.login,
                'password': self.password}

