import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    """Model for user creation"""
    first_name: str
    last_name: str
    username: str
    email: str
    password:str


class UserModel(BaseModel):
    """General user information model"""
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    update_at:datetime


class UserLoginModel(BaseModel):
    """A model for logging a user in to get an access token"""
    email: str
    password: str
