from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
from datetime import datetime
import uuid


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            primary_key=True,
            info={"description": "Unique identifier for the review"},
        ),
    )
    book_id: uuid.UUID = Field(
        foreign_key="books.uid"
    )
    user_uid:uuid.UUID = Field(
        foreign_key="user_accounts.uid"
    )
    rating: float
    review_text: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now))


    