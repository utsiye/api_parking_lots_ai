from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float, UniqueConstraint
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
    user_id = Column(String(255), ForeignKey('users.id'))
    ticket_id = Column(String(255), primary_key=True)
    status = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    messages = Column(JSON, nullable=False)


class Request(Base):
    __tablename__ = 'requests'

    user_id = Column(String(255), ForeignKey('users.id'))
    request_id = Column(String(255), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    source_file_size = Column(Float, nullable=False)
    result_file_size = Column(Float, nullable=False)


class Payment(Base):
    __tablename__ = 'payments'

    user_id = Column(String(255), ForeignKey('users.id'))
    transaction_id = Column(String(255), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    credits = Column(Float, nullable=False)
    balance_total = Column(Integer, nullable=False)
