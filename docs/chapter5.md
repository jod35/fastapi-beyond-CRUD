# Chapter Four: Databases with SQLModel in FastAPI

In the preceding chapter, we developed a functional CRUD API that operated on a simple in-memory database, represented by a Python list. However, in real-world applications, it's essential to use a persistent database to store all necessary data.

## Choosing a Database for FastAPI

FastAPI supports various types of databases, including relational/SQL databases and non-relational/NoSQL databases. Depending on your specific requirements, you can opt for either type.

For this series, we'll focus on using a relational database, specifically PostgreSQL. PostgreSQL is a widely used free and open-source relational database management system, offering numerous benefits:

## Benefits of Using PostgreSQL

- **Advanced Features**: PostgreSQL provides extensive features, including support for complex SQL queries, ACID transactions, and advanced indexing options.

- **Extensibility**: Developers can enhance PostgreSQL's functionality through custom data types, functions, and procedural languages.

- **Scalability**: PostgreSQL efficiently handles large data volumes and high traffic using features like partitioning and parallel query processing.

- **Community Support**: With a large and active community, PostgreSQL enjoys continuous development, support, and knowledge sharing.

- **Security**: Robust security features like SSL encryption and fine-grained access control ensure data integrity and confidentiality.

- **Cross-platform Compatibility**: PostgreSQL is compatible with various operating systems, making it suitable for diverse deployment scenarios.

- **Cost-effectiveness**: Being an open-source solution, PostgreSQL is free to use, resulting in significant cost savings.

- **Compliance**: PostgreSQL adheres to SQL standards and complies with industry regulations such as GDPR and HIPAA.


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

With that in place, we can now set up our configurations so that we can read them out from anywhere within our application. Let us begin by creating a `config.py` file that contains the configuration variables that will be used in this series.

We are going to rely on Pydantic to read our environment variables. Pydantic alone will not help us; we shall need to install `pydantic-settings`, a library that is based on Pydantic to help us with the specific role of reading environment variables from our `.env` file. 


So let us start by installing 

```bash
$ pip install pydantic-settings
```
After installing `pydantic-settings`, let us now go ahead and create a file called `config.py` at the root of our project. Inside that file, add the following code.


```python
# inside the config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///db.sqlite3"
```

### Explanation:

In the provided code snippet, we've performed the following actions:

1. We are importing the `BaseSettings` class from `pydantic_settings`.
2. Creating a subclass called `Settings`, inheriting from `BaseSettings`.
3. Defining an attribute named `DATABASE_URL` with a type annotation of `str`.
4. Setting a default value of `"sqlite:///db.sqlite3"` for `DATABASE_URL`.

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
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///db.sqlite3"

# add this line    
settings = Settings()
```
We add this line so that we don't have to create a new instance of our `Settings` class whenever we shall need to access environment variables. From now on, we shall shall just have to import the `settings` variable and use it.

Alright, let us now connect to our database and also create our table in it. Let us install `sqlmodel`.
```bash
$ pip install sqlmodel
```



**Previous**: [Improved Project Structure Using Routers](./chapter4.md)

**Next**: [Next Chapter](./chapter5.md)

