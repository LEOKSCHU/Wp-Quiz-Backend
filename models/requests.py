from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    password: str = Field(..., description="비밀번호", example="password")

class RegisterRequest(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    password: str = Field(..., description="비밀번호", example="password")
    name: str = Field(..., description="유저 이름", example="test")