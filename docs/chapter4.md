# FastAPI Beyond CRUD (Chapter Four)

## Improved Project Structure Using Routers
Contents of this chapter are
- [Current folder structure](#current-folder-structure)
- [Current code structure](#currrent-code-structure)
- [Restructuring the folder structure](#restructuring-the-project)
- [Introduction to FastAPI Routers](#introduction-to-fastapi-routers)


### Current folder structure
So far, our project structure is quite simple:

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
```

### Currrent code structure
Additionally, our `main.py` file looks like this:

```python
from fastapi import FastAPI, Query
from schemas import BookSchema, BookUpdateSchema

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
    # ... (other book entries)
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

@app.post('/books', status_code=201)
async def create_book(book: BookSchema):
    """Create a new book"""
    books.append(book)
    return book

@app.patch('/book/{book_id}')
async def update_book(book_id: int, update_data: BookUpdateSchema):
    """"Update book"""
    for book in books:
        if book['id'] == book_id:
            book['title'] = update_data.title
            book['author'] = update_data.author
            book['publisher'] = update_data.publisher
            book['page_count'] = update_data.page_count
            book['language'] = update_data.language
            return book
    return {"message": "Book not found"}

@app.delete('/book/{book_id}', status_code=204)
async def delete_book(book_id: int):
    """Delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
```
## Restructuring the project

The problem here is that if we add more code to this file, our code will become messy and hard to maintain. To address this, we need to create a more organized project structure. To start, let's create a new folder called `src`, which will contain an `__init__.py` file to make it a Python package:

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
└── src/
    └── __init__.py
```

Now, create a folder named `books` inside the `src` directory. Inside this folder, add an `__init__.py` file, a `routes.py` file, a `schemas.py` file, and a `book_data.py` file. The `routes.py` file will contain all the book routes, similar to what we created in the previous chapter. The `schemas.py` file will contain the schemas that are currently in our root directory.

```console
├── env/
├── main.py
├── requirements.txt
└── schemas.py
└── src/
    └── __init__.py
    └── books/
        └── __init__.py
        └── routes.py
        └── schemas.py
        └── book_data.py
```

First, let's move our `books` list from `main.py` to `book_data.py` inside the `books` directory.

```python
# Inside book_data.py

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
    # ... (other book entries)
]
```

Next, let's also move our `schemas.py` to the `books` directory.

```python
# Inside schemas.py

from pydantic import BaseModel
from datetime import datetime

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str

class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
```

Now, let's update `routes.py` as follows:

```python
# Inside routes.py

from fastapi import APIRouter
from .book_data import books
from .schemas import BookSchema, BookUpdateSchema

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

@book_router.post('/', status_code=201)
async def create_book(book: BookSchema):
    """Create a new book"""
    books.append(book)
    return book

@book_router.patch('/{book_id}')
async def update_book(book_id: int, update_data: BookUpdateSchema):
    """"Update book"""
    for book in books:
        if book['id'] == book_id:
            book['title'] = update_data.title
            book['author'] = update_data.author
            book['publisher'] = update_data.publisher
            book['page_count'] = update_data.page_count
            book['language'] = update_data.language
            return book
    return {"message": "Book not found"}

@book_router.delete('/{book_id}', status_code=204)
async def delete_book(book_id: int):
    """Delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
```
## Introduction to FastAPI routers 
What has been accomplished is the division of our project into modules using routers. FastAPI routers allow easy modularization of our API by grouping related endpoints together. Routers function similarly to FastAPI instances (similar to what we have in `main.py`). As our project expands, we will introduce additional endpoints, and all of them will be organized into modules grouping related functionalities.

Let's enhance our `main.py` file to adopt this modular structure:

```python

# Inside main.py
from fastapi import FastAPI
from src.books.routes import book_router

version = 'v1'

app = FastAPI(
    title='Bookly',
    description='A RESTful API for a book review service',
    version=version,
)

app.include_router(prefix=f"/api/{version}/books", tags=['books'])
```

Firstly, a variable called `version` has been introduced to hold the API version. Next, we import the `book_router` created in the previous example. Using our FastAPI instance, we include all endpoints created with it by calling the `include_router` method.

Arguments added to the FastAPI instance are:

- `title`: The title of the API.
- `description`: The description of the API.
- `version`  : The version of the API.

While these arguments may not be particularly useful at present, they become valuable when we explore API documentation with **OpenAPI**.

Furthermore, we added the following arguments to the include_router method:

- `prefix`: The path through which all related endpoints can be accessed. In our case, it's named the /{version}/books prefix, resulting in /v1/books or /v2/books based on the application version. This implies that all book-related endpoints can be accessed using http://localhost:8000/api/v1/books.

- `tags`: The list of tags associated with the endpoints that fall within a given router.

### Note:

The current organization of our API is as follows:
| Endpoint	| Method |	Description |
|-----------|--------|--------------|
| /api/v1/books |	GET  | Read all books |
| /api/v1/books |	POST | Create a book |
| /api/v1/books/{book_id} |	GET |	Get a book by ID |
| /api/v1/books/{book_id} |	PATCH |	Update a book by ID |
| /api/v1/books/{book_id} |	DELETE |	Delete a book by ID |


**Previous** [Improved Project Structure Using Routers](./chapter4.md)

**Next** [Databases with SQLModel](./chapter5.md)
