from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    rfidId: Optional[int] = None
    rfidValue: Optional[int] = None