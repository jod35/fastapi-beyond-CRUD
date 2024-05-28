from passlib.context import CryptContext
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import UserCreationModel
from .utils import create_password_hash
from src.config import Config


SECRET_KEY = Config.SECRET_KEY
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, email):
        """get single user"""
        statement = select(User).where(User.email == email)

        result = await self.session.exec(statement)

        book = result.first()

        return book if book else None

    async def get_all_users(self):
        """get all users"""
        statement = select(User).order_by(desc(User.created_at))

        result = await self.session.exec(statement)

        books = result.all()

        return books

    async def create_user(self, user_details: UserCreationModel):
        """create user"""
        user_dict = user_details.model_dump()

        password_hash = create_password_hash(user_dict["password"])

        user_dict["password_hash"] = password_hash

        new_user = User(**user_dict)

        self.session.add(new_user)
        await self.session.commit()

        return new_user
