from dataclasses import dataclass


class PaymentInput:
    id: str = None
    login: str
    password: str
