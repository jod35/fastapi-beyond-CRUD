import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class TagModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime


class TagCreateModel(BaseModel):
    name: str


class TagAddModel(BaseModel):
    tags: List[TagCreateModel]
