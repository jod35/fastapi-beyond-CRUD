from fastapi import FastAPI, Query
from schemas import BookSchema,BookUpdateSchema

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Algorithms and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2021-01-01",
        "page_count": 9282,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Head First HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English",
    },
]




@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/books")
async def read_books():
    return books

@app.get('/book/{book_id}')
async def read_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    return {"message": "Book not found"}

@app.post('/books',status_code=201)
async def create_book(book: BookSchema):
    books.append(book)
    return book

@app.patch('/book/{book_id}')
async def update_book(book_id: int, update_data: BookUpdateSchema):
    for book in books:
        if book['id'] == book_id:
            book['title'] = update_data.title
            book['author'] = update_data.author
            book['publisher'] = update_data.publisher
            book['page_count'] = update_data.page_count
            book['language'] = update_data.language
            return book
    return {"message": "Book not found"}


@app.delete('/book/{book_id}',status_code=204)
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}

