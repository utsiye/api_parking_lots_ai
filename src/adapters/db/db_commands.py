import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.misc.dto.users import UserDTO
from src.adapters.hasher import Hasher
from .models import User, Payment, Ticket, Request


class DBCommands:

    def __init__(self, conn: AsyncSession):
        self.conn: AsyncSession = conn


    async def get_or_create_user(self, user: UserDTO) -> UserDTO:
        print(1)
        query = select(User).where(User.id == user.id)
        res = await self.conn.scalar(query)
        print(res)

        if res:
            return UserDTO(id=res.id, login=res.login, password=res.password)

        if not user.login or not user.password:
            return

        query = select(User).where(User.login == user.login)
        res = (await self.conn.execute(query)).scalars().first()
        print(3)
        if res:
            return
        print(5)
        query = insert(User).values(login=user.login, password=Hasher.get_password_hash(user.password)).returning(User)
        res = (await self.conn.execute(query)).first()
        print(6)
        return UserDTO(id=res.id, login=res.login, password=res.password)

    async def authenticate_user(self, user: UserDTO) -> UserDTO:
        query = select(User).where(User.login == user.login)
        res = await self.conn.execute(query).scalar.first()

        if not res:
            return

        hashed_password = Hasher.get_password_hash(res.password)
        if Hasher.verify_password(res.password, hashed_password):
            return UserDTO(id=res.id, login=res.login, password=res.password)
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
