from fastapi import APIRouter
from src.books.book_data import books
from src.books.schemas import BookSchema,BookUpdateSchema

book_router = APIRouter()

@book_router.get("/")
async def read_books():
    """Read all books"""
    return books

@book_router.get('/{book_id}') 
async def read_book(book_id: int):
    """Read a book"""
    for book in books:
        if book['id'] == book_id:
            return book
    return {"message": "Book not found"}

@book_router.post('/',status_code=201)
async def create_book(book: BookSchema):
    """Create a new book"""
    books.append(book)
    return book

@book_router.patch('/{book_id}')
async def update_book(book_id: int, update_data: BookUpdateSchema):
    """"update book """
    for book in books:
        if book['id'] == book_id:
            book['title'] = update_data.title
            book['author'] = update_data.author
            book['publisher'] = update_data.publisher
            book['page_count'] = update_data.page_count
            book['language'] = update_data.language
            return book
    return {"message": "Book not found"}


@book_router.delete('/{book_id}',status_code=204)
async def delete_book(book_id: int):
    """delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
