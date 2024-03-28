from dataclasses import dataclass

from datetime import datetime


@dataclass
class RequestDTO:
    user_id: int
    request_id: int
    datetime: datetime
    source_file_size: int
    result_file_size: int


@dataclass
class CreateRequestDTO:
    user_id: int
    source_file_size: int
    result_file_size: int
