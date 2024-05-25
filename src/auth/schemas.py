from pydantic import BaseModel
from datetime import datetime
import uuid


class UserCreationModel(BaseModel):
    username: str
    email: str
    password: str


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    created_at: datetime
