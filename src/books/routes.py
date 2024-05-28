from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import BookCreateSchema, BookSchema, BookUpdateSchema
from src.db.main import get_session

from .service import BookService

book_router = APIRouter()


@book_router.get("/", response_model=List[BookSchema])
async def read_books(session: AsyncSession = Depends(get_session)):
    """Read all books"""
    books = await BookService(session).get_all_books()
    return books


@book_router.get("/{book_uid}", response_model=BookSchema)
async def read_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    """Read a book"""
    book = await BookService(session).get_book(book_uid)

    if book is not None:
        return book

    else:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@book_router.post("/", status_code=201, response_model=BookSchema)
async def create_book(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session)
):
    """Create a new book"""
    new_book = await BookService(session).create_book(book)

    return new_book


@book_router.patch("/{book_uid}", response_model=BookSchema)
async def update_book(
    book_uid: str,
    update_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    """ "update book"""

    updated_book = await BookService(session).update_book(book_uid, update_data)

    if not updated_book:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=204)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    """delete a book"""
    result = await BookService(session).delete_book(book_uid)

    if result is not None:
        return {}
    else:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
