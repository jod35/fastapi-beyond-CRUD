from src.auth.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.security import check_password, create_password_hash
from src.auth.schemas import UserCreationModel
from sqlmodel import select, desc


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, email):
        statement = select(User).where(User.email == email)

        result = await self.session.exec(statement)

        book = result.first()

        return book if book else None

    async def get_all_users(self):
        statement = select(User).order_by(desc(User.created_at))

        result = await self.session.exec(statement)

        books = result.all()

        return books

    async def create_user(self, user_details: UserCreationModel):
        user_dict = user_details.model_dump()

        password_hash = create_password_hash(user_dict["password"])

        user_dict["password_hash"] = password_hash

        new_user = User(**user_dict)

        self.session.add(new_user)
        await self.session.commit()

        return new_user
