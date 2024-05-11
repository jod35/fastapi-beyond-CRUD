from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateSchema, BookCreateSchema
from src.db.main import get_session
from .service import BookService

book_router = APIRouter()


@book_router.get("/")
async def read_books(session: AsyncSession = Depends(get_session)):
    """Read all books"""
    books = await BookService(session).get_all_books()
    return books


@book_router.get("/book/{book_uid}")
async def read_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    """Read a book"""
    book = await BookService(session).get_book(book_uid)
    return book


@book_router.post("/", status_code=201)
async def create_book(book: BookCreateSchema, session: AsyncSession = Depends(get_session)):
    """Create a new book"""
    new_book = await BookService(session).create_book(book)

    return new_book


@book_router.patch("/{book_uid}")
async def update_book(
    book_uid: str,
    update_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    """ "update book"""

    updated_book = await BookService(session).update_book(book_uid, update_data)

    return updated_book


@book_router.delete("/{book_uid}", status_code=204)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    """delete a book"""
    await BookService(session).delete_book(book_uid)
    return {}
