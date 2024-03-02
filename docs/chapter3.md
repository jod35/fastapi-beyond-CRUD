# FastAPI Beyond CRUD (Chapter Three)

## Creating a Simple CRUD API

### What is CRUD?

CRUD represents the four basic data operations:

- **Create (C):**

  - _Objective:_ Add new data.
  - _Action:_ Insert a new record or entity.

- **Read (R):**

  - _Objective:_ Retrieve existing data.
  - _Action:_ Fetch data without modification.

- **Update (U):**

  - _Objective:_ Modify existing data.
  - _Action:_ Update attributes or values.

- **Delete (D):**
  - _Objective:_ Remove data.
  - _Action:_ Delete a record or entity.

CRUD operations are fundamental in data management, commonly used in applications dealing with data persistence. In FastAPI Beyond CRUD, the focus is on extending FastAPI capabilities beyond typical CRUD applications, exploring advanced features and use cases. But before diving into such aspects, let us build a simple CRUD API using FastAPI.

Our simple CRUD API will have a few endpoints to perform CRUD operations on a simple in-memory database of books. Here's a list of endpoints that we shall have in our CRUD API.

| Endpoint        | Method | Description         |
| --------------- | ------ | ------------------- |
| /books          | Get    | Read all books      |
| /books          | POST   | Create a book       |
| /book/{book_id} | GET    | Get a book by id    |
| /book/{book_id} | PATCH  | Update a book by id |
| /book/{book_id} | DELETE | Delete a book by id |

The provided table describes various API endpoints, their associated HTTP methods, and their functionalities:

1. **`/books` - GET: Read all books**

   - _Description:_ This endpoint is designed to retrieve information about all available books. When a client makes an HTTP GET request to `/books`, the server responds by providing details on all books in the system.

2. **`/books` - POST: Create a book**

   - _Description:_ To add a new book to the system, clients can make an HTTP POST request to `/books`. This operation involves creating and storing a new book based on the data provided in the request body.

3. **`/book/{book_id}` - GET: Get a book by id**

   - _Description:_ By making an HTTP GET request to `/book/{book_id}`, clients can retrieve detailed information about a specific book. The `book_id` parameter in the path specifies which book to fetch.

4. **`/book/{book_id}` - PATCH: Update a book by id**

   - _Description:_ To modify the information of a specific book, clients can send an HTTP PATCH request to `/book/{book_id}`. The `book_id` parameter identifies the target book, and the request body contains the updated data.

5. **`/book/{book_id}` - DELETE: Delete a book by id**
   - _Description:_ This endpoint allows clients to delete a specific book from the system. By sending an HTTP DELETE request to `/book/{book_id}`, the book identified by `book_id` will be removed from the records.

Now that we have a plan of our simple API, we can now build our simple CRUD API by adding the following code to `main.py`. We shall begin by creating a very simple list of books that we will use as our database.

```python
# in memory database of the books
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
```

Once we have that, we shall build our endpoints on the simple database.

```python
rom fastapi import FastAPI, Query
from schemas import BookSchema,BookUpdateSchema

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

## What happened?

The first API endpoint is `/books` and it's purpose is to read all the books in the database and return a list of them. we achive that by creating a function `read_books` that will return our `books` list.

```python
@app.get("/books")
async def read_books():
    return books
```

FastAPI really makes it easy to return any JSON serializable object in a response.

### Note

JSON (JavaScript Object Notation) serialization is the process of converting a data structure or object from a programming language (such as Python, JavaScript, or others) into a JSON-formatted string. This string representation can then be transmitted over a network or stored in a file, and later deserialized back into the original data structure.

For Python, the following data types are serializable.

- Lists
- Dictionaries
- Strings
- Tuples
- Bools
- None

So this makes it possible for us to just return a list of our book objects when we make a `GET` request to `http://localhost:8000/books` as showed below
![list books](./imgs/img5.png)

We retrieve a single book by its ID by calling the `read_book` function whenever we make a request to `book/{book_id}`. Note that the {book_id} is refered to as a **path parameter** that is even passed to the `read_book function to find the book with the given ID. All we have done is to iterate through the book list, and check if a book exists in the list with the given ID. If not found,, we shall return a message indicating that.

```python
@app.get('/book/{book_id}')
async def read_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    return {"message": "Book not found"}
```

![get a book](./imgs/img6.png)

In order to add a new book to our system, we must first define a schema class. FastAPI leverages Pydantic for creating such schema classes, offering robust data validation and serialization capabilities for API endpoints. This ensures that incoming data is validated according to predefined rules, and the data objects exchanged with the database are efficiently serialized.

Let's take a closer look at the process. We'll create a new schema class for books, aligning its structure with the attributes found in our existing list of books. This schema class will be created in a file named schemas.py. The code for our `BookSchema` class is as follows:

```python
from pydantic import BaseModel
from datetime import datetime

class BookSchema(BaseModel):
    id:int
    title:str
    author:str
    publisher:str
    published_date: datetime
    page_count:int
    language:str
```

The class `BookSchema` defines a Pydantic model that inherits from `BaseModel`. Pydantic is a data validation library that provides a concise way to define the schema classes using [type annotations](https://peps.python.org/pep-0484/)

The class has the following attributes:

- `id` : The integer unique identifier for the book.
- `title`: The string title of the book.
- `author`: The string author of the book.
- `publisher`: The string publisher of the book.
- `published_date`: The datetime for when the book was published. It is of type `datetime` from the `datetime` module.
- `page_count`: The integer number of pages in the book.
- `language`: The string language in which the book is written.

So the folowing is the endpoint for creating a book, it takes data as expected by the schema we have created in the previous step and appends it to our books list. This adds validation to the data we send to the server.

```python
@app.post('/books',status_code=201)
async def create_book(book: BookSchema):
    books.append(book)
    return book
```

The `BookSchema` class implements validation for the book data we send to the server in this POST request. As a result, summitting invalid data will result into validation errors as shown in the figure below. This error will show up when no data is sent to the server.

![validation for no data being sent to the server](./imgs/img7.png)


Let us also try to submit invalid data to the server that has a field missing.

![Validation for invalid data being sent to the server](./imgs/img8.png)

Finally, let us submit valid JSON data to the server. This will created a new book record and as we can notice, a 201 Created status code will be returned in our response as shown below.

![Successful creation od the new book record with valid JSON data](./imgs/img9.png)

### Note
It is so important that you return the correct HTTP status code in every response, to achieve that, you should provide the `status_code` parameter every time you create an endpoint as shown below. The default status code will always be the 200 status code returned by the server in case of a successful response.
```python
@app.post('/books',status_code=201)
```

Let us look at the update endpoint. This is quite similar to the create endpoint as it allows data to be sent to the server via the **PATCH** HTTP method. But it also requires we provide the `book_id` of the book that we will be updating. we loop through the book list and find the book that matches the `book_id` as shown below:

```python
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
```

If you notice, we have added the `update_data` parameter to our handler function and this is to be the validator for the data we shall use to update the book record. Notice this has a different schema called `BookUpdateSchema`. In our **schemas.py**, let us add the following code.

```python
class BookUpdateSchema(BaseModel):
    title:str
    author:str
    publisher:str
    page_count:int
    language:str
```

Notice how we have neglected some of the fields that are available in our Book structure as shown in our list of books. This is to ensure that we only send those fields that will be updated. Let us update our book record.

![successful updated of a book record](./imgs/img10.png)

Let us confirm if our book record has been updated successfully. To do so we are going to retrieve the book by its ID. The book record has been updated successfully.

![retrieve updated book record](./imgs/img11.png)

Let us finally look at deletion of the book record. This is carried out in the following example:

```python
@app.delete('/book/{book_id}',status_code=204)
async def delete_book(book_id: int):
    """delete a book"""
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    return {"message": "Book not found"}
```
What we have here is to loop through the books and find the book associated with the given `book_id` the we remove it from the list of books by using the `remove` list method. Notice that we are return a 204 response status code. This means that we have deleted the book and therefore we shall not return any content as shown below.

![delete a book record ](./imgs/img12.png)


And just like that, we have created a CRUD REST API using a simple in memory database. 





**Previous** [Creating a Simple Web Server](./index.md)

**Next** [Next Chapter](./chapter4.md)
