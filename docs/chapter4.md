# FastAPI Beyond CRUD (Chapter Four)

## A better Project Structure
For now, we have a very simple project structure that looks like this;

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
```

And also our `main.py` file, looks like this:

```python
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




@app.get("/books")
async def read_books():
    """Read all books"""
    return books

@app.get('/book/{book_id}')
async def read_book(book_id: int):
    """Read a book"""
    for book in books:
        if book['id'] == book_id:
            return book
    return {"message": "Book not found"}

@app.post('/books',status_code=201)
async def create_book(book: BookSchema):
    """Create a new book"""
    books.append(book)
    return book

@app.patch('/book/{book_id}')
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


@app.delete('/book/{book_id}',status_code=204)
async def delete_book(book_id: int):
    """delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
```

The problem we have here is that if we at all we add more code to this file, our code will be messed up as it will be all in one place. To fix this we shall have to create a much more organized project structure. To begin, we shall create a new folder called `src`, This will contain a `__init__.py` file that will make it a Python package. 

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
|__ src/
    |__ __init__.py
```

Let us create a folder called `books` that shall contain all source code that will be related to books. Inside the folder, create a `__init__.py` file. Also add a `routes.py` and a `schemas.py` file. The `routes.py` file will contain all the book routes like we created in the [previous Chapter](./chapter3.md). In side the `schema.py`, we shall add the schemas that are currently in our root directory.

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
|__ src/
    |__ __init__.py
    |__ books/
        |__ __init__.py
        |__ routes.py
        |__ schemas.py
```

Let us change `routes.py` to include the following.
```python
from fastapi import APIRouter
from .book_data import books

book_router = APIRouter(

)

@app.get("/books")
async def read_books():
    """Read all books"""
    return books

@app.get('/book/{book_id}')
async def read_book(book_id: int):
    """Read a book"""
    for book in books:
        if book['id'] == book_id:
            return book
    return {"message": "Book not found"}

@app.post('/books',status_code=201)
async def create_book(book: BookSchema):
    """Create a new book"""
    books.append(book)
    return book

@app.patch('/book/{book_id}')
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


@app.delete('/book/{book_id}',status_code=204)
async def delete_book(book_id: int):
    """delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
```
