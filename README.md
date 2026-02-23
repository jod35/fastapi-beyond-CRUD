# FastAPI Beyond CRUD

This is the source code for the [FastAPI Beyond CRUD](https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&si=rl-08ktaRjcm2aIQ) course. The course focuses on FastAPI development concepts that go beyond the basic CRUD operations.

For more details, visit the project's [website](https://jod35.github.io/fastapi-beyond-crud-docs/site/).

## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [CI/CD Pipelines](#cicd-pipelines)
7. [Contributing](#contributing)

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
    git clone https://github.com/manmohan659/fastapi-beyond-CRUD.git
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

Alternatively, run the entire stack using Docker (no extra setup or downloads needed):

```bash
docker compose up
```

This starts PostgreSQL, Redis, the FastAPI web server (with automatic migrations), and the Celery worker. The API is available at http://localhost:8000/api/v1/docs.

## Running Tests
Run the tests using this command:

```bash
pytest src/tests/ -v
```

## CI/CD Pipelines

This project includes two GitHub Actions workflows.

### 1. PR Conventional Commits Check

**Trigger:** Every pull request (opened, updated, reopened).

**What it does:**
- Validates that all commits in the PR follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
- If any commit does not comply, the PR is **automatically closed** with a comment listing the offending commits.
- An email notification is sent to the PR author (extracted from git commit metadata).

**Conventional Commit format:**
```
type(scope): description
```

Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### 2. Nightly Build

**Trigger:** Every day at midnight UTC (cron), or manually via `workflow_dispatch`.

**What it does:**
- Checks out the `main` branch and runs the test suite.
- If tests **pass**: builds a Docker image and pushes it to GitHub Container Registry (GHCR) with tags `nightly`, `nightly-YYYYMMDD`, and `nightly-<sha>`.
- If tests **fail**: the image is NOT pushed, and an email notification is sent to the repository owner.

**Container image:** `ghcr.io/manmohan659/fastapi-beyond-crud:nightly`

### Required GitHub Secrets

Both workflows use SMTP for email notifications. Configure these secrets in **Settings > Secrets and variables > Actions**:

| Secret | Description | Example (Ethereal) |
|---|---|---|
| `SMTP_SERVER` | SMTP server hostname | `smtp.ethereal.email` |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USERNAME` | SMTP login username | `your-user@ethereal.email` |
| `SMTP_PASSWORD` | SMTP login password | `your-ethereal-password` |
| `NOTIFICATION_EMAIL` | Recipient for nightly build failure alerts | `you@example.com` |

**Quick setup with Ethereal (free):**
1. Go to https://ethereal.email/ and click "Create Ethereal Account".
2. Copy the generated SMTP credentials into the GitHub Secrets above.
3. View captured emails at https://ethereal.email/messages.

## Contributing
I welcome contributions to improve the documentation! You can contribute [here](https://github.com/jod35/fastapi-beyond-crud-docs).

## License

This project is for educational purposes as part of the [FastAPI Beyond CRUD](https://youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P&si=rl-08ktaRjcm2aIQ) course by Ssali Jonathan.

## Acknowledgements

Built as part of the CS463/663 course assignment.
