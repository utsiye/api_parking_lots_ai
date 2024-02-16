from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src.misc.dto.users import UserDTO
from src.services.hasher import Hasher
from .models import User, Payment, Ticket, Request
import src.exceptions.classes as exceptions


class DBCommands:

    def __init__(self, conn: AsyncSession):
        self.conn: AsyncSession = conn

    async def get_or_create_user(self, user: UserDTO) -> UserDTO:
        if user.id:
            query = select(User).where(User.id == user.id)
            res = await self.conn.scalar(query)
            if res:
                return UserDTO(id=res.id, login=res.login, password=res.password, balance=res.balance)

        is_user_exists = await self._is_user_exists(user.login)
        if is_user_exists:
            raise exceptions.user.UserIsAlreadyExistsException()

        if not user.login or not user.password:
            raise exceptions.common.MissingRequiredParameterException()

        query = insert(User).values(login=user.login, password=Hasher.get_password_hash(user.password)).returning(User)
        res = await self.conn.scalar(query)
        await self.conn.commit()
        return UserDTO(id=res.id, login=res.login, password=res.password, balance=res.balance)

    async def authenticate_user(self, user: UserDTO) -> UserDTO:
        query = select(User).where(User.login == user.login)
        res = await self.conn.scalar(query)

        if not res:
            raise exceptions.UnauthorizedException()

        if Hasher.verify_password(user.password, res.password):
            return UserDTO(id=res.id, login=res.login, password=res.password)
        else:
            raise exceptions.UnauthorizedException()

    async def update_user_password(self, user_id: int, new_password: str) -> UserDTO:

        query = update(User).where(User.id == user_id).values(password=Hasher.get_password_hash(new_password)).returning(User)
        res = await self.conn.scalar(query)
        await self.conn.commit()

        return UserDTO(id=res.id, login=res.login, password=res.password, balance=res.balance)

    async def update_user(self, user_id: int, **kwargs) -> UserDTO:
        if 'password' in kwargs.keys():
            await self.update_user_password(user_id, new_password=kwargs['password'])
            del kwargs['password']

        query = update(User).where(User.id == user_id).values(**kwargs).returning(User)
        res = await self.conn.scalar(query)
        await self.conn.commit()

        return UserDTO(id=res.id, login=res.login, password=res.password, balance=res.balance)

    async def _is_user_exists(self, login: str) -> bool:
        query = select(User).where(User.login == login)
        res = await self.conn.scalar(query)

        if res:
            return True
        else:
            return False
