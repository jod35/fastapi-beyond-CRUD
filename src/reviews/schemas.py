from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class ReviewModel(BaseModel):
    uid: uuid.UUID 
    rating: int = Field(lt=5)
    review_text : str
    user_uid: Optional[uuid.UUID] 
    book_uid: Optional[uuid.UUID] 
    created_at: datetime
    update_at: datetime

class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text : str