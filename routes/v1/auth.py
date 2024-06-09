from fastapi import APIRouter, HTTPException, Header
from typing import Annotated, Optional, Union


from models.requests import LoginRequest, RegisterRequest
from models.responses import LoginResponse, RegisterResponse, UserResponse
from utils.auth import generate_token, register_account, verify_token
from utils import db
# from utils import auth

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=LoginResponse, status_code=200)
async def _login(Request: LoginRequest):
    return LoginResponse(**{"accessToken": await generate_token(Request.email, Request.password)})

@auth_router.post("/register", response_model=RegisterResponse, status_code=200)
async def _register(Request: RegisterRequest):
    if await register_account(Request.email, Request.password, Request.name):
        return RegisterResponse(**{"detail":"OK"})

@auth_router.get("/me", response_model=UserResponse, status_code=200)
async def _me(Authorization: Optional[str] = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Unauthorized | 인증되지 않았습니다.")
    res = await verify_token(Authorization)
    username = res.get("username")
    user = await db.get_user(username)
    return UserResponse(**{"email":user.get("username"), "name":user.get("name")})
