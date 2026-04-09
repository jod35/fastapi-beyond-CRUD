from enum import Enum
from typing import Optional
from pydantic import BaseModel

class MemberStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    REJECTED = "rejected"


class Member(BaseModel):
    id: int
    first_name: str
    last_name: str
    address: str
    phone_number: str
    national_id_number: str
    occupation: str
    status: MemberStatus
    group_id: Optional[int] = None
