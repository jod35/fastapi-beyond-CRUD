from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class Author(SQLModel, table=True):
    __tablename__ = "authors"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            primary_key=True,
            info={"description": "Unique identifier for the author"},
        )
    )

    name: str
    biography: str = Field(max_length=400)
    nationality: str

    def __repr__(self) -> str:
        return f"{self.name}"
