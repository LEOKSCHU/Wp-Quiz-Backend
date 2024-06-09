from pydantic import BaseModel, Field

class LoginResponse(BaseModel):
    accessToken: str = Field(..., description="JWT 토큰", example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MjYwNjIwNzB9.7")

class RegisterResponse(BaseModel):
    detail: str = Field(..., description="설명", example="OK")

class UserResponse(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    name: str = Field(..., description="유저 이름", example="test")