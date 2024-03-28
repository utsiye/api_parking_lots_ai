import datetime

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float, UniqueConstraint, ARRAY, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    balance = Column(Integer, nullable=False, default=0)


class Ticket(Base):
    __tablename__ = "tickets"

    user_id = Column(Integer, ForeignKey('users.id'))
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255), nullable=False, default="in progress")
    datetime = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    ticket_id = Column(Integer, ForeignKey('tickets.ticket_id'))
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


class Request(Base):
    __tablename__ = 'requests'

    user_id = Column(Integer, ForeignKey('users.id'))
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    source_file_size = Column(Float, nullable=False)
    result_file_size = Column(Float, nullable=False)


class Payment(Base):
    __tablename__ = 'payments'

    user_id = Column(Integer, ForeignKey('users.id'))
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    credits = Column(Integer, nullable=False)
    balance_total = Column(Integer, nullable=False)
