import uuid
from datetime import datetime

from pydantic import BaseModel


class UserCreationModel(BaseModel):
    username: str
    email: str
    password: str


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    created_at: datetime


class UserLoginModel(BaseModel):
    email: str
    password: str
