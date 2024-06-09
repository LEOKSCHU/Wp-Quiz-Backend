from typing import List
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    password: str = Field(..., description="비밀번호", example="password")

class RegisterRequest(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    password: str = Field(..., description="비밀번호", example="password")
    name: str = Field(..., description="유저 이름", example="test")


class CreateQuizRequest(BaseModel):
    title: str = Field(..., description="퀴즈 제목", example="테스트")
    description: str = Field(..., description="퀴즈 설명", example="테스트")
    author: str = Field(..., description="작성자", example="test")
    img: str = Field(..., description="이미지 Base64", example="image/png;base64,....")
    tags: dict = Field(..., description="태그", example=["테스트", "테스트2"])
    quizzes: dict

class SubmitQuizRequest(BaseModel):
    session: str = Field(..., description="세션 ID", example="UUID")
    answers: dict = Field(..., description="답안", example={"1":1, "2":2, "3":3, "4":4, "5":5})