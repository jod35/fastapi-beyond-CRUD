from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
import uuid


class Book(SQLModel , table=True):
    __tablename__ = "books"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the book"},
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language:str

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        return f"<Book {self.title}>"