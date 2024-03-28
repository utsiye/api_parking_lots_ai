from dataclasses import dataclass

from datetime import datetime


@dataclass
class PaymentDTO:
    transaction_id: int
    datetime: datetime
    credits: int
    balance_total: int
