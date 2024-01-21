import random
import string

import asyncpg

from .dto.users import UserDTO
from app.services.hasher import Hasher


class DBCommands:

    def __init__(self, conn: asyncpg.Connection):
        self.conn: asyncpg.Connection = conn

    async def get_or_create_user(self, _id: str = None, login: str = None, password: str = None) -> UserDTO:
        res = await self.conn.fetchrow("SELECT * FROM users WHERE id=$1", _id)

        if res:
            return UserDTO(id=res.get('id'), login=res.get('login'), password=res.get('password'))

        if not login or not password:
            return

        _id = await self._generate_id('users')
        res = await self.conn.fetchrow('INSERT INTO users VALUES ($1, $2, $3) RETURNING *',
                                       _id, login, Hasher.get_password_hash(password))

        return UserDTO(id=res.get('id'), login=res.get('login'), password=res.get('password'))

    async def authenticate_user(self, login: str, password: str) -> UserDTO:
        res = await self.conn.fetchrow("SELECT * FROM users WHERE login=$1", login)

        if not res:
            return

        hashed_password = Hasher.get_password_hash(res.get('password'))
        if Hasher.verify_password(res.get('password'), hashed_password):
            return UserDTO(id=res.get('id'), login=res.get('login'), password=res.get('password'))
        else:
            return

    async def _is_object_id_exist(self, _id: str, table_name: str) -> bool:
        res = await self.conn.fetchrow(f"SELECT id FROM {table_name} WHERE id=$1", _id)

        if res:
            return True
        else:
            return False

    async def _generate_id(self, table_name: str) -> str:

        for i in range(100):
            characters = string.ascii_uppercase + string.digits
            generate_id = ''.join(random.choice(characters) for _ in range(6))
            if not await self._is_object_id_exist(generate_id, table_name):
                return generate_id
