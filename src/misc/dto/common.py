from dataclasses import dataclass


@dataclass
class PaginationDTO:
    limit: int = 100
    skip: int = 0
