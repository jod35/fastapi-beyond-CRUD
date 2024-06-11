from .models import User
from .schemas import UserCreateModel
from .utils import generate_passwd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user
    

    async def get_all_users(self, session:AsyncSession):
        """get all users"""
        statement = select(User).order_by(desc(User.created_at))

        result = await session.exec(statement)

        books = result.all()

        return books