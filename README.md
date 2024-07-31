# FastAPI Beyond CRUD 
This is source code for the [FastAPI Beyond CRUD](https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&si=rl-08ktaRjcm2aIQ) course. This course focuses on FastAPI Development concepts beyond the CRUD stuff.

For more details, you can visit the project [website](https://jod35jon.github.io/fastapi-website/site/).

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)



## Getting Started
Provide instructions on how to set up and run your FastAPI project.

### Prerequisites
This project requires that you have the following dependencies

- Python >= 3.10
- PostgreSQL
- Redis


### Project setup
Begin by cloning the project
```console
git clone https://github.com/jod35/fastapi-beyond-CRUD.git
```
Enter your project
```console
cd fastapi-beyond-CRUD/
```

Create your virtualenv and activate it with
```console
python3 -m venv env 
```
activate the virtualenv with
```console
source env/bin/activate
```
Install all project dependencies with

```console
pip install -r requirements.txt
```

All environment variable are located in this [file](./.env.example
), so it is important you add them in a `.env` file before you run the server.


Next, run database migrations
```console
alembic upgrade head
```

Open another terminal within your virtualenv and run a celery worker (in a Linux / Unix shell please)  
```console
sh runworker.sh
```

Finally run your the application.

```console
fastapi dev src/
```

To run tests
```console
pytest
```

