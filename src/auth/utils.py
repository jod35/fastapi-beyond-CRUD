from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.config import Config

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Check and verify your password against a hash"""
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_password_hash(plain_password: str) -> str:
    """Hash a password to be stored in the database"""
    return PASSWORD_CONTEXT.hash(plain_password)


def create_access_token(data: dict, expires: timedelta | None = None):
    """Create new access token for authorization"""
    data = data.copy()

    now = datetime.now()

    if not expires:
        expires = timedelta(minutes=30)

    data.update({"exp": now + expires})

    token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return token


def decode_token(token: str) -> dict | None:
    """Get data from an access token"""

    try:
        data = jwt.decode(token, SECRET_KEY)
        return data

    except Exception:
        return {}


def get_user_from_jwt(token: str) -> str | None:
    """Get user from  a given JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not (username := payload.get("sub")):
            return None

    except jwt.PyJWTError:
        return None

    return username
