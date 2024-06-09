from pydantic import BaseModel, Field
from typing import List

from models.quiz import Question, Quiz, userQuestion

class LoginResponse(BaseModel):
    accessToken: str = Field(..., description="JWT 토큰", example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MjYwNjIwNzB9.7")

class RegisterResponse(BaseModel):
    detail: str = Field(..., description="설명", example="OK")

class UserResponse(BaseModel):
    email: str = Field(..., description="유저 email", example="test@example.com")
    name: str = Field(..., description="유저 이름", example="test")

class QuizData(BaseModel):
    id: str = Field(..., description="퀴즈 ID", example=1)
    title: str = Field(..., description="퀴즈 제목", example="테스트")
    description: str = Field(..., description="퀴즈 설명", example="테스트")
    author: str = Field(..., description="작성자", example="test")
    questionsCount: int = Field(..., description="문제 수", example=10)
    image: str = Field(..., description="이미지 URL", example="https://example.com/image.jpg")
    tags: List[str] = Field(..., description="태그", example=["테스트", "테스트2"])

class SearchQuizResponse(BaseModel):
    data: List[QuizData]

class QuizResponse(BaseModel):
    name: str = Field(..., description="퀴즈 이름", example="테스트")
    quiz: list[userQuestion]
    session: str = Field(..., description="세션 ID", example="UUID")