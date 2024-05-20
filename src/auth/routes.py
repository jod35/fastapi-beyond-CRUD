from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse


auth_router = APIRouter()

basic = HTTPBasic()

@auth_router.get('/login')
async def login_user(user_creds: HTTPBasicCredentials= Depends(basic)):
    test_username = "jona"
    test_password = "p455w0rd"
    
    user = user_creds.username
    password = user_creds.password

    if (user == test_username) and (password == test_password):
        return {"username":user , "password":password}

    return JSONResponse(content={"error":"Invalid username or password"}, status_code=status.HTTP_400_BAD_REQUEST)