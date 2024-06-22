from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import BookCreateModel, BookModel, BookUpdateModel
from src.db.main import get_session
from src.auth.dependencies import security

from .service import BookService

book_router = APIRouter()

session = Depends(get_session)
book_service = BookService()


@book_router.get("/", response_model=List[BookModel], dependencies=[Depends(security)])
async def read_books(session: AsyncSession = session):
    """Read all books"""
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/{book_uid}", response_model=BookModel, dependencies=[Depends(security)]
)
async def read_book(book_uid: str, session: AsyncSession = session):
    """Read a book"""
    book = await book_service.get_book(book_uid, session)

    if book is not None:
        return book

    else:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@book_router.post(
    "/", status_code=201, response_model=BookModel, dependencies=[Depends(security)]
)
async def create_book(book_data: BookCreateModel, session: AsyncSession = session):
    """Create a new book"""
    new_book = await book_service.create_book(book_data, session)

    return new_book


@book_router.patch(
    "/{book_uid}", response_model=BookModel, dependencies=[Depends(security)]
)
async def update_book(
    book_uid: str,
    update_data: BookUpdateModel,
    session: AsyncSession = session,
):
    """ "update book"""

    updated_book = await book_service.update_book(book_uid, update_data, session)

    if not updated_book:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    else:
        return updated_book


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(security)],
)
async def delete_book(book_uid: str, session: AsyncSession = session):
    """delete a book"""
    result = await book_service.delete_book(book_uid, session)

    if result is not None:
        return {}
    else:
        raise HTTPException(
            detail={"error": "book not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
