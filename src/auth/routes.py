from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .utils import create_access_token, check_password
from .service import UserService
from .auth_handler import security
from typing import List


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.get(
    "/users", status_code=status.HTTP_200_OK, response_model=List[UserModel]
)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)

    return users


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None and check_password(password, user.password_hash):
        access_token = create_access_token({"user_id": str(user.uid)})

        return {"message": "Login Successful", "token": access_token, "user": user}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email Or Password"
        )


@auth_router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_token():
    pass


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_users():
    pass
