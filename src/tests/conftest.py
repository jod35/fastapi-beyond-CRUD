from unittest.mock import MagicMock
from src import app
from src.db.main import get_session
import pytest



mock_session = MagicMock()

def overried_get_session():
    try:
        yield mock_session

    finally:
        pass


app.dependency_overrides[get_session] = mock_session


@pytest.fixture
def mock_db_session():
    return mock_session


