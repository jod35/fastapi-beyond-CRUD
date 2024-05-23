from passlib.context import CryptContext


PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'],deprecated="auto")


def check_password(plain_password:str, hashed_password:str) -> bool:
    return PASSWORD_CONTEXT.verify(plain_password,hashed_password)


def create_password_hash(plain_password:str) -> str:
    return PASSWORD_CONTEXT.hash(plain_password)


