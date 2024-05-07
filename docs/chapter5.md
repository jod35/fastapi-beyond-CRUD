# FastAPI Beyond CRUD (Chapter Five)

## Databases with SQLModel
Contents of this chapter are
- [Choosing a database for FastAPI](#current-folder-structure)
- [Choosing a Database for FastAPI](#choosing-a-database-for-fastapi)
- [Explaining Object-Relational Mappers (ORMs)](#explaining-an-object-relational-mapper-orm)
- [Creating a Database (PostgreSQL)](#creating-a-database)
- [Settings Management With Pydantic](#settings-management-with-pydantic)
- [Creating database models with SQLModel](#creating-database-models-with-sqlmodel)
- [Connecting to databases](#connecting-to-databases)
- [Lifespan events in FastAPI](#lifespan-events-in-fastapi)
- [Creating database tables](#creating-database-tables)

In the preceding chapter, we developed a functional CRUD API that operated on a simple in-memory database, represented by a Python list. However, in real-world applications, it's essential to use a persistent database to store all necessary data.

## Choosing a Database for FastAPI

FastAPI supports various types of databases, including relational/SQL databases and non-relational/NoSQL databases. Depending on your specific requirements, you can opt for either type.

For this series, we'll focus on using a relational database, specifically PostgreSQL. PostgreSQL is a widely used free and open-source relational database management system, offering numerous benefits:

While using PostgreSQL, we shall need to choose a way to interact with the database using the Python Language. That introduces us to the concept of an [Object Relational mapper](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping).

## Explaining an Object-Relational Mapper (ORM)

An Object-Relational Mapper (ORM) serves as a translator between a programming language, such as Python, and a database, like PostgreSQL or MySQL.

In simpler terms, think of an ORM as an interpreter in a conversation where one person speaks English (Python) and the other speaks French (database). The ORM understands both languages, allowing you to interact with the database using familiar Python code without needing to understand the intricacies of how the database works internally.

### How it Works:

1. **Mapping Objects to Tables**: You create Python classes to represent tables in the database. Each object of these classes corresponds to a row in the database table.

2. **Interacting with Data**: You can then interact with these Python objects as if they were regular objects in your code, like setting attributes and calling methods.

3. **Behind the Scenes**: When you perform operations on these objects, like saving or deleting, the ORM translates these actions into the appropriate SQL queries that the database understands.

4. **Data Conversion**: The ORM handles converting Python data types into database-specific types and vice versa, ensuring compatibility between the two.

An ORM simplifies the process of working with databases by allowing you to focus on your application's logic in Python, rather than getting bogged down in SQL queries and database management details. It acts as a bridge between the object-oriented world of programming and the relational world of databases.

There are several different ORM solutions available for Python, but the most popular is [SQLAlchemy](https://sqlalchemy.org). SQLAlchemy simplifies database access and manipulation by providing an ORM for mapping Python objects to database tables and offering a high-level SQL expression language for querying databases. While SQLAlchemy is a powerful tool on its own, there's an ORM solution that seamlessly integrates SQLAlchemy with Pydantic, the data validation library discussed in previous chapters.


## Creating a Database
In this series, we will make use of [SQLModel](https://sqlmodel.tiangolo.com/), a library tailored for FastAPI. Interestingly, it was developed by the same individual who created FastAPI.

Let's initiate the database setup. Setting up a database can be intricate, often involving multiple steps. Fortunately, numerous options are available that simplify the database creation process without extensive configuration.

Throughout this course, I'll utilize [Neon](https://neon.tech/), a free fully managed PostgreSQL database with a generous free tier. With Neon, we can swiftly create a database and get started without delay.

![image of Neon](./imgs/neon.png)

Once you have created your free account on Neon, you can create a new project and in it, you will also create your new database.

![Create a new project and database](./imgs/neon2.png)

Once you have created your database, you can then go ahead and copy your connection details. 
![Copy your connection details](./imgs/neon3.png)


After, Create a file called `.env` in which we shall store our project configurations as secrets. (This file is important and should not be added to version control) In your `.env` file, paste the database connection URL you have obtained from Neon. We are going to create an environment variable called `DATABASE_URL` with the value of our URL.

```bash
# inside .env
DATABASE_URL=postgresql://bookdb_owner:w8JK2sCASYBc@ep-rough-block-a554nxl6.us-east-2.aws.neon.tech/bookdb?sslmode=require
```


At this point, your folder structure needs to look something like this:
```console
|__ .env
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
### Settings Management With Pydantic
With that in place, we can now set up our configurations so that we can read them out from anywhere within our application. Let us begin by creating a `config.py` file that contains the configuration variables that will be used in this series.

We are going to rely on Pydantic to read our environment variables. Pydantic alone will not help us; we shall need to install `pydantic-settings`, a library that is based on Pydantic to help us with the specific role of reading environment variables from our `.env` file. 


So let us start by installing 

```bash
$ pip install pydantic-settings
```
After installing `pydantic-settings`, let us now go ahead and create a file called `config.py` at the root of our project. Inside that file, add the following code.


```python
# inside src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str ="sqlite:///db.sqlite3"

    model_config = SettingsConfigDict(
        env_file=".env"
    )
```

### Explanation:

In the provided code snippet, we've performed the following actions:

1. We are importing the `BaseSettings` class from `pydantic_settings`.
2. Creating a subclass called `Settings`, inheriting from `BaseSettings`.
3. Defining an attribute named `DATABASE_URL` with a type annotation of `str`.
4. Setting a default value of `"sqlite:///db.sqlite3"` for `DATABASE_URL`.
5. To modify our configuration to read from the `.env` file, we modified the `model_config` attribute of the `Settings` class which is one to help us with modifying the configuration of any pydantic model class. This is set to an instance of the `SettingsConfigDict` class which enables us to read the configuration from the `.env` file. This is by simply setting the `env_file` argument to the name of the `.env` file.

This configuration allows us to read the `DATABASE_URL` from the environment variables. If it's not provided, it falls back to the default value, `"sqlite:///db.sqlite3"`.

Let's observe how this configuration operates. We'll initiate a Python interpreter shell for testing:

```bash
$ python3
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from config import Settings
>>> settings = Settings()
>>> settings.DATABASE_URL
'postgresql://bookdb_owner:w8JK2sCASYBc@ep-rough-block-a554nxl6.us-east-2.aws.neon.tech/bookdb?sslmode'
>>> 
```

In the above demonstration, we start by importing the `Settings` class from the `config.py` file. Subsequently, we instantiate a `settings` object. Utilizing this `settings` object, we access and retrieve the `DATABASE_URL` setting. Upon calling it, our database URL will be displayed in the console. Note that this shall work because we currently have the `DATABASE_URL` setting in our `.env` file.

Once this has been implemented, let us then add the following line to `config.py`.
```python
# inside src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

# add this line    
Config = Settings()
```
We add this line so that we don't have to create a new instance of our `Settings` class whenever we shall need to access environment variables. From now on, we shall shall just have to import the `Config` variable and use it.


## Creating database models with SQLModel

Alright, let us now connect to our database and also create our table in it. Let us install `sqlmodel`.
```bash
$ pip install sqlmodel
```

Once we have `sqlmodel` installed, let us now create a database model using it. to start, we will create a file named models.py inside the `books` directory.

```console
|__ .env
├── env/
├── main.py
├── requirements.txt
└── schemas.py
└── src/
    └── __init__.py
    └── books/
        └── __init__.py
        └── routes.py
        |__ models.py
        └── schemas.py
        └── book_data.py
```
Inside `models.py`, add the following code. 
```python
# inside src/books/models.py
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class Book(SQLModel , table=True):
    __tablename__ = "books"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False
        )
    )

    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language:str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        return f"<Book {self.title}>"

```

### Explanation
IN the above code, we have defined a database model using `SQLModel`. Here are the steps we took. 
1. We imported the `SQLModel`, `Field`, `Column` from sqlmodel.
2. We import `sqlalchemy.dialects.postgresql`as `pg` to allow us access the PostgreSQL-specific column types.
3. In the model definition, we create a `Book` class that inherits from `SQLModel`, we then also add the `table` parameter to the class and set it to `True`to inidicate that the class is going to represent a database table.

    #### Note
        All SQLModel models are pydantic tables and therefore can be used for data validation.

4. Inside the class, several attributes are defined:
    - `uid`: A universally unique identifier (UUID) for each book. We use the `Field` function, to add some details or attributes to it. It's also specified as the primary key column `(primary_key=True)`, with a default value generated by `uuid.uuid4()`, and it's unique and not nullable.

    #### Note
        To make our primary key store UUIDs, we have chosen to use the PostgreSQL UUID type and we achive this by using the sa_column argument in the Field function. Using SQLALchemy's Column class we then specify the type of the field.
    
    - `title`, `author`, `publisher`, `published_date`, `page_count`, `language`: These attributes represent various properties of a book, such as title, author, publisher, etc. They are all specified as strings (str) or integers (int) and will be columns in the database table.

    - `created_at` and `updated_at` represent timestamps at which a book record was created or updated. Note that we are also going in detail about defining the PostgreSQL column types as `pg.TIMESTAMP`. We also specify that we want to keep track of the 

    - def __repr__(self) -> str: This is a special method that defines how instances of the `Book` class are represented as strings. In this case, it returns a string containing the title of the book, enclosed in angle brackets and preceded by `Book`.


## Connecting to databases
For now, our current directory structure looks something like this.
```
├── README.md
├── requirements.txt
├── run.py
└── src
    ├── books
    │   ├── book_data.py
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   └── schemas.py
    ├── config.py
    └── __init__.py
```

Let us add a directory in our `src` folder and call it `db` (short for database). we shall make it a normal Python package by adding the `__init__.py` file. After, we shall go ahead and add a Python file called `main.py` and we shall then add the following code.

```python
# inside src/db/main.py
from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """create a connection to our db"""

    async with engine.begin() as conn:
        statement = text("select 'Hello World'")

        result = await conn.execute(statement)

        print(result)
```
### Explanation
1. We begin by importing the necessary objects from the libraries they belong to.

    ```python
    # inside src/db/main.py
    from sqlmodel import create_engine, text
    from sqlalchemy.ext.asyncio import AsyncEngine
    from src.config import Config
    ```
    `create_engine` is a function that enables to connect to a database when we need. `text` is a function that helps us generate plain text SQL statements that we can run against a database when we connect to it. `AsyncEngine` is a class for creating asynchronous engine objects. We shall look at how we shall use it in a moment. `Config` is the settings objects we created above. This will allow us access our configurations.


2.  We then create the `engine` object. This will allow us to connect to the database when we need to. (We will look at how we will use it later.)
    ```python
    engine = AsyncEngine(create_engine(
        url=Config.DATABASE_URL,
        echo=True
    ))
    ```
    This object is created by calling the `create_engine()` function. In the function call, we also add two important argumnents. The first argument is the `url` to the database to connect to. In this case, we shall use the `DATABASE_URL` value from the configuration we set up above. This is accessed on the `Config` object created in our settings.
    
    
    The second argument is the `echo` argument, this allows us to log SQL statements that will be executed in the database everytime they are executed. We finally create this object inside the `AsyncEngine` class because we want to be able to interact with the database using an asynchronous DBAPI. 

        A DBAPI (Database Application Programming Interface) is simply a medium through which the Python programming language can connect to the database server.

3. Finally, we create a function called `initdb` which is responsible for connecting to the database and executing a simple SQL statement. 

    ```python
    async def initdb():
    """create a connection to our db"""

    async with engine.begin() as conn:
        statement = text("select 'Hello World'")

        result = await conn.execute(statement)

        print(result.all())
    ```

    Inside the `initdb` function, we begin by creating a connection object `conn` using an async context manager. (created with `async with engine.begin()`). We then create a plain text SQL statement and call the `text` function.

    The result of the statement is what we access through the `result` object which we finally print to our terminal when we call the `all` method on it.



## Lifespan events in FastAPI

In FastAPI, we are free to define logic we may want to run before the application starts getting requests and also when the application stops receiving them. THis is very important in scenarios where the cost of running such logic may be expensive and may cause a poor user experience. Such include database connections, loading AI models and so on. For our purpose, we are going to connect to the database before the application starts. If this doesn't make sense, let us begin by looking at a small example. 

In the `__init__.py` file at the root of the `src` directory, let us modify the code as shown below.

```python
# src/__init__.py
from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager


#the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):    
    print("Server is starting...")
    yield
    print("server is stopping")



app = FastAPI(
    lifespan=lifespan # add the lifespan event to our application
)

app.include_router(
    book_router,
    prefix="/books",
    tags=['books']
)


```

### Explanation

Let's create an async function called lifespan. This function will be decorated with asynccontextmanager from the contextlib module in Python. Inside this function, there will be two print statements, separated by a `yield` statement.

The code before the `yield` statement will execute first (when the server starts), followed by the code after the `yield` statement, which will execute last (when the server stops).

This function is a **lifespan event** because it runs once before the application starts and then continues throughout the application's lifespan.

Now, if we stop the server by pressing *CTRL+C* and then restart it, the following output will be logged in the terminal.
```console
$ python3 run.py 
INFO:     Will watch for changes in these directories: ['/home/jod35/Documents/fastapi-beyond-CRUD']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press *CTRL+C* to quit)
INFO:     Started reloader process [18506] using WatchFiles
INFO:     Started server process [18508]
INFO:     Waiting for application startup.
server is starting...
```
At the server's start, you'll observe the text `server is starting` printed in the terminal. After halting the server using *Ctrl+C*, you should see the subsequent output
```console
INFO:     Application startup complete.
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
server is stopping
INFO:     Application shutdown complete.
INFO:     Finished server process [18669]
$
```

Now that we grasp how lifespan events function, let's integrate our init_db function to establish a connection to the PostgreSQL database.

Update the lifespan function in `src/__init__.py` to include the following code.

```python
#src/__init__.py
...
from src.db.main import initdb


@asynccontextmanager
async def lifespan(app: FastAPI):    
    await initdb()
    yield
    print("server is stopping")
```
Upon saving, you'll observe the following output in your terminal.

```console
INFO:     Started server process [21034]
INFO:     Waiting for application startup.
2024-05-06 11:50:41,802 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-05-06 11:50:41,803 INFO sqlalchemy.engine.Engine select 'Hello World'
2024-05-06 11:50:41,803 INFO sqlalchemy.engine.Engine [generated in 0.00015s] ()
[('Hello World',)]
2024-05-06 11:50:41,803 INFO sqlalchemy.engine.Engine COMMIT

```
This code establishes a connection to the database and executes a SELECT statement, which will return the string "Hello World" as demonstrated in the provided output.


## Creating database tables
Let's update the code in `src/db/main.py` to incorporate our custom lifespan event into the database model, utilizing the `Book` model. We'll then utilize SQLmodel to generate the necessary database tables based on this model.

```python
# inside src/db/main.py
from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel import SQLModel
from src.books.models import Book


engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """create our database models in the database"""

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

In the above code, we began with importing the `Book` model from `src/books/models`. After, we then modify the `initdb()` function by adding the following:
```python
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

```

In this code snippet, we utilize an asynchronous context manager with `engine.begin()`, enabling us to create a transactional context to interact with our database. Within this context, we execute `conn.run_sync(SQLModel.metadata.create_all()`.

Here, `SQLModel.metadata` encompasses all the metadata linked with SQLModel. By invoking the `create_all()` method on this metadata object, any tables present in the metadata but absent in the database will be created.

**Note** 
- `conn.run_sync()` is an asynchronous function that we utilize to run synchronous functions such as `SQLModel.metadata.create_all()`.


With that said, let us save the file and have a look at our terminal output. 
```console
INFO:     Waiting for application startup.
2024-05-06 12:13:21,042 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-05-06 12:13:21,042 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("books")
2024-05-06 12:13:21,042 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-05-06 12:13:21,043 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("books")
2024-05-06 12:13:21,043 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-05-06 12:13:21,044 INFO sqlalchemy.engine.Engine 
CREATE TABLE books (
        uid UUID NOT NULL, 
        title VARCHAR NOT NULL, 
        author VARCHAR NOT NULL, 
        publisher VARCHAR NOT NULL, 
        published_date VARCHAR NOT NULL, 
        page_count INTEGER NOT NULL, 
        language VARCHAR NOT NULL, 
        created_at TIMESTAMP, 
        updated_at TIMESTAMP, 
        PRIMARY KEY (uid), 
        UNIQUE (uid)
)


2024-05-06 12:13:21,044 INFO sqlalchemy.engine.Engine [no key 0.00014s] ()
2024-05-06 12:13:21,086 INFO sqlalchemy.engine.Engine COMMIT
```
Running the code above shall allow us to create the table in the database also logging the SQL query in the terminal as shown above. 

### Conclusion
The database for storing our book data is now up and running. Skipping ahead, I've outlined the CRUD actions for our persistent database in the next chapter.


**Previous**: [Improved Project Structure Using Routers](./chapter4.md)

**Next**: [Next Chapter](./chapter5.md)

