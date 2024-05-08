# FastAPI Beyond CRUD (Chapter Four)

# Finishing Up the CRUD
Contents of this chapter are
- [Creating a service class](#creating-a-service-class)
- [Creating a new book](#creating-a-new-book)
- [Retrieving a book by its uid](#retrieve-a-book-by-its-uid)
- [Update a book](#update-a-book)
- 


## Creating a service class
In this chapter, we will focus on creating a dedicated service file to house the essential logic required for executing CRUD operations using our PostgreSQL database. The primary objective is to abstract away database interactions from our API routes, enhancing code readability and maintainability.

We will construct a class within this service file, which will serve as a centralized point for invoking all methods related to managing our book data.

To initiate this process, let's commence by creating the file `service.py` within the `src/books/` directory.
```python

from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreateModel
from sqlmodel import select


class BookService:
    """
    This class provides methods to create, read, update, and delete books
    """

    pass

```

We call this class `BookService` as it shall be called only when managing data about books. We then create an `__init__` method to help us define some attributes on this class. The first attribute we give to this class is the `session` object. In SQLModel, a session object is **a unit of work** through which all of transactions between the database and Python are done. Through it we can Create, Read, Update, Delete database objects in an efficient manner.

Let us add this to our `BookService` class.
```python
    ... #the rest of the BookService class
    def __init__(self, session: AsyncSession):
        self.session = session
```

Every `BookService` instance shall be created with a `session` object allowing it to interact with the database.


### Read all books
Let us begin by adding the method `get_all_books` that is responsible for getting all the books from the database.

```python
    ... #the rest of the BookService class
    async def get_all_books(self):
        """
        Get a list of all books

        Returns:
            list: list of books
        """
        statement = select(Book).order_by(Book.created_at)

        result = await self.session.exec(statement)

        return result.all()
```

To start, we craft a query utilizing the `select` function from SQLModel, initiating an SQL **SELECT** operation on our Books table. Subsequently, we sort the books based on their creation date (**created_at**) via the **order_by** method.

This constructed statement is subsequently executed through the `session` object, assuming that we have assigned an attribute to objects that will be instantiated from our class. The resulting `result` object will return a list of books obtained by invoking the `all` method.

### Creating a new Book
Let us now add the method for creating a new book
```python
    ... # rest of the BookService class
    async def create_book(self, book_create_data: BookCreateModel):
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
```
The `create_book` method is responsible for adding a new book to the database using the provided book data. Specifically, `book_create_data` must adhere to the structure defined by a Pydantic model called `BookCreateModel`, which we'll soon create in our `src/books/schema.py` directory.


To create a new book record, we begin by initializing a new instance of the Book database model. This is achieved by unpacking book_create_data, which we convert into a Python dictionary utilizing the model_dump method.

Following this, we utilize our `session` object to add the new book record to the database via `session.add`. Finally, we commit the transaction to ensure that the changes are persisted in the database, accomplished with `session.commit`, not forgetting to return the newly created book record.

Before we proceed, we need to add the `BookCreateSchema` class to `src/books/schemas.py` 

Let us add the `BookCreateSchema` class to `src/books/schemas.py`.
```python
# inside src/books/schemas.py
class BookCreateModel(BaseModel):
    """
        This class is used to validate the request when creating or updating a book
    """
    title: str
    author: str
    isbn: str
    description: str
```


### Retrieve a book by its uid
```python
    ... # the rest of the BookService class
    async def get_book(self, book_uid: str):
        """Get a book by its UUID.

        Args:
            book_uid (str): the UUID of the book

        Returns:
            Book: the book object
        """
        statement = select(Book).where(Book.uid == book_uid)

        result = await self.session.exec(statement)

        return result.first()
```

To retrieve a book from the database, we construct a select statement to fetch all books but filter by the uid to ensure that only the desired book is retrieved. This filtering is achieved using the where method.

Subsequently, we execute the statement using the session object, obtaining the result. Finally, we retrieve the book by invoking the first method on the result object.

### Update a book
Now updating a book is going to involve the following:
- first, we need to retrieve the book to update by its `uid`
- second, we need to get the data we shall be updating the book with.
- finally, we shall update the book fields with the new data
- return the updated book



```python
    async def update_book(self, book_uid: str, book_update_data: BookCreateModel):
        """Update a book

        Args:
            book_uid (str): the UUID of the book
            book_update_data (BookCreateModel): the data to update the book

        Returns:
            Book: the updated book
        """

        statement = select(Book).where(Book.uid == book_uid)

        result = await self.session.exec(statement)

        book = result.first()

        for key, value in book_update_data.model_dump().items():
            setattr(book, key, value)

        await self.session.commit()

        return book

```
To implement the `update_book` method, which updates a book by its UID, we first fetch the book based on its UID, following the approach described for retrieving a book.

Next, we update the book object with the following code:

```python
# Unpack the book data dictionary and set fields
for key, value in book_update_data.model_dump().items():
    setattr(book, key, value)
```

This code iterates over the key-value pairs in the dictionary obtained from `book_update_data.model_dump()`, setting each field of the book object accordingly.



Finally, after updating the book object with the new data, we commit the changes to the database using session.commit(). This ensures that the modifications made to the book are saved persistently in the database.


### Delete a Book
To delete a book from the database, we follow a similar approach as when retrieving a book. Once we have obtained the book object from the database using its UID, we use the session.delete method to mark the book object for deletion. To finalize the deletion and apply the changes to the database, we call session.commit(). This ensures that the book is effectively removed from the database.

```python
    async def delete_book(self, book_uid):
        """Delete a book

        Args:
            book_uid (str): the UUID of the book
        """
        statement = select(Book).where(Book.uid == book_uid)
        result = await self.session.exec(statement)

        book = result.first()

        await self.session.delete(book)

        await self.session.commit()
```


Let update our routes to ensure they use our newly created book database to Create, Read, Update and Delete our book database record. The source code for `src/books/service.py` should look like this at this point.

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from .schemas import BookCreateModel
from sqlmodel import select


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
        statement = select(Book).order_by(Book.created_at)

        result = await self.session.exec(statement)

        return result.all()

    async def create_book(self, book_create_data: BookCreateModel):
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

        return result.first()

    async def update_book(self, book_uid: str, book_update_data: BookCreateModel):
        """Update a book

        Args:
            book_uid (str): the UUID of the book
            book_update_data (BookCreateModel): the data to update the book

        Returns:
            Book: the updated book
        """

        statement = select(Book).where(Book.uid == book_uid)

        result = await self.session.exec(statement)

        book = result.first()

        for key, value in book_update_data.model_dump().items():
            setattr(book, key, value)

        await self.session.commit()

        return book

    async def delete_book(self, book_uid):
        """Delete a book

        Args:
            book_uid (str): the UUID of the book
        """
        statement = select(Book).where(Book.uid == book_uid)
        result = await self.session.exec(statement)

        book = result.first()

        await self.session.delete(book)

        await self.session.commit()
```

## Dependency Injection
Now that we have created the `BookService` class, we need to create the `session` object that we shall use a dependency in every API route that shall interact with the database in any way.

Dependency injection in FastAPI allows for the sharing of state among multiple API routes by providing a mechanism to create Python objects, referred to as **dependencies**, and accessing them only when necessary within dependant functions. While the concept may initially seem technical and esoteric, it is a fundamental aspect of FastAPI that proves remarkably beneficial across various scenarios. Interestingly, we often employ dependency injection without realizing it, demonstrating its widespread usefulness. Some potential applications include:

- Gathering input parameters for HTTP requests (Path and query parameters)
- Validating parameters inputs
- Checking authentication and authorization (we shall look at this in coming chapters)
- Emitting logs and metrics e.t.c.


Let us create our first dependency:
```python
# add this to src/db/main.py
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

... # rest of main.py

async def get_session() -> AsyncSession:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
```

In the above code, we define an async function called `get_session` that should return an object of the `AsyncSesion` class. This class is what allows us to use an aync DBAPI to interact with the database. That is the object we shall create all `BookService` objects with.




Now that we have an understanding of how we shall get our session, let us go to the `src/books/routes.py` and modify it to make calls to the methods we have so far defined inside the `BookService` class.

```python
# inside src/books/routes.py
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateSchema
from src.db.main import get_session
from .service import BookService

book_router = APIRouter()


@book_router.get("/")
async def read_books(session: AsyncSession = Depends(get_session)):
    """Read all books"""
    books = await BookService(session).get_all_books()
    return books


@book_router.get("/{book_id}")
async def read_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    """Read a book"""
    book = await BookService(session).get_book(book_uid)
    return book


@book_router.post("/", status_code=201)
async def create_book(book: BookSchema, session: AsyncSession = Depends(get_session)):
    """Create a new book"""
    new_book = await BookService(session).create_book(book)

    return new_book


@book_router.patch("/{book_id}")
async def update_book(
    book_uid: int,
    update_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    """ "update book"""

    updated_book = await BookService(session).update_book(book_uid, update_data)

    return updated_book


@book_router.delete("/{book_id}", status_code=204)
async def delete_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    """delete a book"""
    await BookService(session).delete_book(book_uid)
    return {}
```

We've made minimal changes to the file but have introduced some updates that I'll outline here. Let's start by examining the dependency injection we've integrated. Take note of how we've included the following code in each route handler function.
```python
session: AsyncSession = Depends(get_session)
```
What we're accomplishing here is the sharing of the `session` generated by calling the `get_session` function we defined earlier in this chapter.

Once the `session` is established, we proceed to instantiate the `BookService` class. This instance allows us to utilize its methods for performing various **CRUD** operations as needed.

```python
    books = await BookService(session).get_all_books()
```
We instantiate the `BookService` function to invoke its `get_all_books()` method, supplying the session as a dependency to the route handler that includes the above code.