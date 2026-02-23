# FastAPI Beyond CRUD 

This is the source code for the [FastAPI Beyond CRUD](https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&si=rl-08ktaRjcm2aIQ) course. The course focuses on FastAPI development concepts that go beyond the basic CRUD operations.

For more details, visit the project's [website](https://jod35.github.io/fastapi-beyond-crud-docs/site/).

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [Contributing](#contributing)

## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL
- Redis

### Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/jod35/fastapi-beyond-CRUD.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd fastapi-beyond-CRUD/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```

6. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

7. Open a new terminal and ensure your virtual environment is active. Start the Celery worker (Linux/Unix shell):
    ```bash
    sh runworker.sh
    ```

## Running the Application
Start the application:

```bash
fastapi dev src/
```
Alternatively, you can run the application using Docker:
```bash
docker compose up -d
```
## Running Tests
Run the tests using this command
```bash
pytest
```

## GitHub Actions CI/CD

This project includes two GitHub Actions workflows:

### 1. Conventional Commits Check
Triggered on every Pull Request. Validates that all commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. If any commit is non-compliant, the PR is automatically closed and an email notification is sent.

### 2. Nightly Build
Runs every night at 12:00 AM UTC (or manually via `workflow_dispatch`). Runs the test suite first — if tests pass, a Docker image is built and pushed to the GitHub Container Registry (`ghcr.io`). If tests fail, the build is aborted and an email notification is sent.

### Required GitHub Secrets
Set these under **Settings > Secrets and variables > Actions** in your repository:

| Secret | Description |
|---|---|
| `ETHEREAL_EMAIL` | Ethereal SMTP username (create at https://ethereal.email/create) |
| `ETHEREAL_PASSWORD` | Ethereal SMTP password |
| `NOTIFICATION_EMAIL` | Recipient email address for failure notifications |

### Required GitHub Settings
- Go to **Settings > Actions > General > Workflow permissions**
- Select **Read and write permissions** (needed for pushing images to GHCR)

## Contributing
I welcome contributions to improve the documentation! You can contribute [here](https://github.com/jod35/fastapi-beyond-crud-docs).
