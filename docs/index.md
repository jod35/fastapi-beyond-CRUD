# Fast API Beyond CRUD (Chapter One)

## Installation and Configuration

In this section, we will guide you through the installation process of FastAPI for this course, starting with a minimal setup.

### 1. Virtual Environment Creation

Begin by creating a virtual environment using the built-in Python library `venv`. If you already have Python installed, you might not need to install it separately. However, on Linux, installation may be necessary based on your distribution.

```bash
python3 -m venv env
```

This command generates a virtual environment in the specified folder (in our example, `env`). Activate the virtual environment using the following commands:

On Linux or macOS:
```bash
source env/bin/activate
```

On Windows:
```bash
env/Scripts/activate
```

Once activated, your command line will indicate the active virtual environment:

On Linux or macOS:
```bash
(env) yourusername@yourmachine$
```

On Windows:
```bash
(env) C:\users\YourUsername>
```

### 2. Directory Structure
At this point, your directory structure should look like this:

```
└── env
```

### 3. Dependency Installation

Now, install the essential dependencies within the virtual environment. We need `fastapi` as our web framework and `uvicorn` as the web server for running the FastAPI application.

```bash
(env) pip install fastapi uvicorn
```

### 4. Freeze Dependencies

Freeze the installed dependencies into a `requirements.txt` file to track the exact versions for reproducibility.

```bash
(env) pip freeze > requirements.txt
```

By following these steps, you have successfully set up a virtual environment, installed FastAPI and Uvicorn, and frozen the dependencies for future reference. This structured approach ensures a clean and manageable development environment for our FastAPI project.

**Next** [Creating a Simple Web Server](./chapter2.md)
