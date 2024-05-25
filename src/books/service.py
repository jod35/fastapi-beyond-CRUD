from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from .schemas import BookCreateSchema
from sqlmodel import select, desc


class BookService:
    """
    This class provides methods to create, read, update, and delete books
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        """
        Get a list of all books

        Returns:
            list: list of books
        """
        statement = select(Book).order_by(desc(Book.created_at))

        result = await self.session.exec(statement)

        return result.all()

    async def create_book(self, book_create_data: BookCreateSchema):
        """
        Create a new book

        Args:
            book_create_data (BookCreateModel): data to create a new

        Returns:
            Book: the new book
        """
        new_book = Book(**book_create_data.model_dump())

        self.session.add(new_book)

        await self.session.commit()

        return new_book

    async def get_book(self, book_uid: str):
        """Get a book by its UUID.

        Args:
            book_uid (str): the UUID of the book

        Returns:
            Book: the book object
        """
        statement = select(Book).where(Book.uid == book_uid)

        result = await self.session.exec(statement)

        book = result.first()

        return book if book else None

    async def update_book(self, book_uid: str, book_update_data: BookCreateSchema):
        """Update a book

        Args:
            book_uid (str): the UUID of the book
            book_update_data (BookCreateModel): the data to update the book

        Returns:
            Book: the updated book
        """

        book = await self.get_book(book_uid=book_uid)

        if book is not None:
            for key, value in book_update_data.model_dump().items():
                setattr(book, key, value)

            await self.session.commit()

            return book

        else:
            return None

    async def delete_book(self, book_uid):
        """Delete a book

        Args:
            book_uid (str): the UUID of the book
        """
        book = await self.get_book(book_uid=book_uid)

        if book is not None:
            await self.session.delete(book)

            await self.session.commit()

            return {}

        else:
            return None
