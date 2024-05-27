from passlib.context import CryptContext
from src.config import Config
from src.auth.models import User
import jwt

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Check and verify your password against a hash"""
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_password_hash(plain_password: str) -> str:
    """Hash a password to be stored in the database"""
    return PASSWORD_CONTEXT.hash(plain_password)


def create_access_token(user_details:dict):
    token  = jwt.encode(
        user_details,
        SECRET_KEY,
        ALGORITHM
    )

    return token



def get_user_from_jwt(token: str) -> str | None:
    """Get user from  a given JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not (username:=payload.get('sub')):
            return None

    except jwt.PyJWTError as e:
        return None
    
    return username
    




