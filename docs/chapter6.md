# FastAPI Beyond CRUD (Chapter Four)

# Finishing Up the CRUD
Contents of this chapter are
- [Creating a service class](#creating-a-service-class)
- [Creating a new book](#creating-a-new-book)
- [Retrieving a book by its uid](#retrieve-a-book-by-its-uid)
- [Update a book](#update-a-book)
- 


## Creating a service class
In this chapter, we shall Create a service file, in which we shall add all logic that is necessary for implementing the **CRUD** using our PostgreSQL database. The reasoning behind this is to separate the database logic from our API routes making our code simpler to read and maintain.

We shall create a class on which all methods for managing our book data will be called.

Let us begin creating the file service.py inside `src/books/`
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

FastAPI provides a dependency injection mechanism that allows us share state among many different api routes. Let us see how we can do this.

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

In the above code, we define an async function called `get_session` that should return an object of the `AsyncSesion` class. This class is what allows us to use an aync DBAPI to interact with the database.




Let us go to the `src/books/routes.py` and modify it to make calls to the methods we have so far defined inside the `BookService` class.

```python

```