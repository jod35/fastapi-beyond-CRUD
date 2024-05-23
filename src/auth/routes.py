from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.schemas import UserCreationModel, UserSchema
from src.auth.service import UserService
from typing import List


auth_router = APIRouter()

basic = HTTPBasic()



@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreationModel, session: AsyncSession = Depends(get_session)
):

    username = user_data.username
    email = user_data.email
    password = user_data.password

    user = await UserService(session).get_user(email)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "User Account Already Exists"},
        )
    else:
        new_user = await UserService(session).create_user(user_data)
        return {"message": "User Created successfully"}


@auth_router.get(
    "/users", status_code=status.HTTP_200_OK, response_model=List[UserSchema]
)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await UserService(session).get_all_users()

    return users
