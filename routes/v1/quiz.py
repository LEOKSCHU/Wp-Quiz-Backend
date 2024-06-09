from fastapi import APIRouter, HTTPException, Header
from typing import Annotated, Optional, Union
import datetime
import random
from uuid import uuid4

from models.quiz import Quiz, Question, userQuestion
from models.requests import CreateQuizRequest, LoginRequest, RegisterRequest, SubmitQuizRequest
from models.responses import LoginResponse, QuizResponse, RegisterResponse, SearchQuizResponse, UserResponse
from utils.auth import generate_token, register_account, verify_token
from utils import db
# from utils import auth

quiz_router = APIRouter(prefix="/quiz")

@quiz_router.get("/search", response_model=SearchQuizResponse, status_code=200)
async def _search(query: Optional[str] = ""):
    data = await db.search_quiz(query)
    data = [Quiz(**quiz) for quiz in data]
    return SearchQuizResponse.parse_obj({"data":data})

@quiz_router.post("/create", status_code=200)
async def _create(Request: CreateQuizRequest):
    quizId = str(abs(hash(datetime.datetime.now().timestamp())))
    questions = [Question(id=int(key), question=Request.quizzes[key]["title"], answers=list(Request.quizzes[key]["answers"].values()), answer=int(Request.quizzes[key]["answer"])-1) for key in Request.quizzes.keys()]
    quiz = Quiz(**{"id":quizId, "title":Request.title, "description":Request.description, "author":Request.author, "image": Request.img, "tags": list(Request.tags.values()),"questions":questions, "questionsCount":len(Request.quizzes.keys())})
    await db.create_quiz(quiz.dict())
    return {"id":quizId}

@quiz_router.get("/{quizId}",response_model=QuizResponse, status_code=200)
async def _getQuiz(quizId: str, quizCount: int = 5):
    print(quizId, quizCount)
    data = await db.find_one("quiz", "id", quizId)
    quiz = random.sample([question for question in data.get("questions")], quizCount)
    for i in range(len(quiz)):
        quiz[i]["id"] = i+1
    uuid = uuid4()
    await db.save_session(uuid, quiz)
    return QuizResponse(name=data.get("title"), quiz=quiz, session=str(uuid))

@quiz_router.post("/submit", status_code=200)
async def _submitQuiz(Request: SubmitQuizRequest):
    data = await db.find_one("sessions", "uuid", Request.session)
    answers = list(Request.answers.values())
    quiz = data.get("quiz")
    score = 0
    for i in range(len(quiz)):
        if quiz[i]["answer"] == answers[i]:
            score += 1
    return {"correct":score, "total":len(quiz)}