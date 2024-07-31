from fastapi.testclient import TestClient
from src import app

client = TestClient(app)


version_prefix = "/api/v1"


def test_create_user(mock_db_session):
    response = client.post(
        f"{version_prefix}/signup",
        json={
            "username": "jod35",
            "email": "jodestrevin@gmail.com",
            "first_name": "jonathan",
            "last_name": "ssali",
            "password": "test123",
        },
    )

    assert mock_db_session.add_called()
    assert mock_db_session.commit_called()


def test_login(mock_db_session):
    response = client.post(
        f"{version_prefix}/login",
        json={"email": "jodestrevin@gmail.com", "password": "test123"},
    )

    assert mock_db_session.exec_called()