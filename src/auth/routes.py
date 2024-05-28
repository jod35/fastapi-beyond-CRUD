from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreationModel, UserSchema, UserLoginModel
from .utils import create_access_token, check_password
from .service import UserService
from .auth_handler import security
from typing import List


auth_router = APIRouter()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreationModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user = await UserService(session).get_user(email)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "User Account Already Exists"},
        )
    else:
        new_user = await UserService(session).create_user(user_data)
        return {"message": "User Created successfully", "user": new_user}


@auth_router.get(
    "/users", status_code=status.HTTP_200_OK, response_model=List[UserSchema]
)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await UserService(session).get_all_users()

    return users


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await UserService(session).get_user(email)

    if user is not None and check_password(password, user.password_hash):
        access_token = create_access_token({"user_id": str(user.uid)})

        return {"message": "Login Successful", "token": access_token, "user": user}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email Or Password"
        )


@auth_router.post("/me")
async def current_user(user_creds: HTTPAuthorizationCredentials = Depends(security)):
    return {"message": "Current user"}


@auth_router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_token():
    pass


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_users():
    pass
