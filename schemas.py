from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    first_name: str
    surname: str
    email: str
    phone_number: str
    national_id: str
    gender: str
    date_of_birth: str


class Customer(CustomerCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    national_id: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
