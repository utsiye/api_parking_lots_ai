import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src.misc.dto.users import UserDTO
from src.misc.dto.payments import PaymentDTO
from src.misc.dto.common import PaginationDTO
from src.misc.dto.requests import RequestDTO, CreateRequestDTO
from src.misc.dto.tickets import TicketDTO, CreateTicketDTO, MessageDTO
from src.services.hasher import Hasher
from .models import User, Payment, Ticket, Request, Message
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

    async def create_request(self, request: CreateRequestDTO) -> RequestDTO:
        query = insert(Request).values(user_id=request.user_id, source_file_size=request.source_file_size,
                                       result_file_size=request.result_file_size).returning(Request)
        res = await self.conn.scalar(query)

        await self.conn.commit()

        return RequestDTO(user_id=res.user_id, request_id=res.request_id, datetime=res.datetime,
                          source_file_size=res.source_file_size, result_file_size=res.result_file_size)

    async def create_ticket(self, ticket: CreateTicketDTO) -> TicketDTO:
        query = insert(Ticket).values(user_id=ticket.user_id).returning(Ticket)
        ticket_res = await self.conn.scalar(query)

        query = insert(Message).values(ticket_id=ticket_res.ticket_id, text=ticket.text).returning(Message)
        message_res = await self.conn.scalar(query)

        await self.conn.commit()

        message = MessageDTO(message_id=message_res.message_id, text=message_res.text, datetime=message_res.datetime)
        return TicketDTO(user_id=ticket_res.user_id, ticket_id=ticket_res.ticket_id, messages=[message],
                         status=ticket_res.status, datetime=ticket_res.datetime)

    async def update_ticket(self, ticket_id: int, **kwargs) -> TicketDTO:  # TODO delete if not necessary
        query = update(Ticket).where(Ticket.ticket_id == ticket_id).values(**kwargs).returning(Ticket)
        ticket_res = await self.conn.scalar(query)

        await self.conn.commit()

        messages = await self.get_ticket_messages(ticket_id)

        return TicketDTO(user_id=ticket_res.user_id, ticket_id=ticket_res.ticket_id, messages=messages,
                         status=ticket_res.status, datetime=ticket_res.datetime)

    async def add_ticket_message(self, ticket_id: int, text: str) -> TicketDTO:
        query = insert(Message).values(ticket_id=ticket_id, text=text).returning(Message)
        res = await self.conn.scalar(query)

        await self.conn.commit()

        ticket = await self.get_ticket(ticket_id)
        return ticket

    async def get_ticket_messages(self, ticket_id: int) -> list[MessageDTO]:
        query = select(Message).where(Message.ticket_id == ticket_id)
        message_res = await self.conn.scalars(query)

        messages = [MessageDTO(message_id=message.message_id, text=message.text,
                               datetime=message.datetime) for message in message_res]
        return messages

    async def get_ticket(self, ticket_id: int) -> TicketDTO:
        query = select(Ticket).where(Ticket.ticket_id == ticket_id)
        ticket_res = await self.conn.scalar(query)

        if not ticket_res:
            raise exceptions.TicketNotFoundException

        messages = await self.get_ticket_messages(ticket_id)

        return TicketDTO(user_id=ticket_res.user_id, ticket_id=ticket_res.ticket_id, messages=messages,
                         status=ticket_res.status, datetime=ticket_res.datetime)

    async def get_all_user_payments(self, user_id: int, pagination: PaginationDTO) -> list[PaymentDTO]:
        query = select(Payment).where(Payment.user_id == user_id).limit(pagination.limit).offset(pagination.skip)
        res = await self.conn.scalars(query)

        if res:
            payments_list = [PaymentDTO(transaction_id=payment.transaction_id, datetime=payment.datetime,
                                        credits=payment.credits, balance_total=payment.balance_total) for payment in res]
            return payments_list
        else:
            return []

    async def get_payment(self, user_id: int, transaction_id: int) -> PaymentDTO:
        query = select(Payment).where(Payment.transaction_id == transaction_id and Payment.user_id == user_id)
        res = await self.conn.scalar(query)

        if not res:
            raise exceptions.PaymentNotFoundException
        return PaymentDTO(transaction_id=res.transaction_id, datetime=res.datetime,
                          credits=res.credits, balance_total=res.balance_total)

    async def get_all_user_requests(self, user_id: int, pagination: PaginationDTO) -> list[RequestDTO]:
        query = select(Request).where(Request.user_id == user_id).limit(pagination.limit).offset(pagination.skip)
        res = await self.conn.scalars(query)

        if res:
            requests_list = [RequestDTO(request_id=request.transaction_id, datetime=request.datetime,
                                        source_file_size=request.source_file_size,
                                        result_file_size=request.result_file_size) for request in res]
            return requests_list
        else:
            return []

    async def get_request(self, user_id: int, request_id: int) -> RequestDTO:
        query = select(Request).where(Request.request_id == request_id and Request.user_id == user_id)
        res = await self.conn.scalar(query)

        if not res:
            raise exceptions.RequestNotFoundException
        return RequestDTO(request_id=res.transaction_id, datetime=res.datetime,
                          source_file_size=res.source_file_size, result_file_size=res.result_file_size)

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

        query = update(User).where(User.id == user_id).values(password=Hasher.get_password_hash(new_password)).returning(
            User)
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
