from dataclasses import dataclass

from datetime import datetime


@dataclass
class TicketDTO:
    user_id: int
    ticket_id: int
    messages: list
    status: str
    datetime: datetime


@dataclass
class CreateTicketDTO:
    user_id: int
    text: str


@dataclass
class MessageInput:
    description: str


@dataclass
class MessageDTO:
    message_id: int
    text: str
    datetime: datetime
