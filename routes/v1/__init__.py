from fastapi import APIRouter
from .auth import auth_router

# from .users import users_router

v1_router = APIRouter()
v1_router.include_router(auth_router, tags=["auth"])
# v1_router.include_router(users_router, prefix="/users", tags=["users"])
