from pydantic import BaseModel

class userQuestion(BaseModel):
    id: int 
    question: str
    answers: list[str]

class Question(userQuestion):
    answer: str

class Quiz(BaseModel):
    id: str
    title: str
    description: str
    author: str
    questionsCount: int
    image: str
    tags: list[str]
    questions: list[Question]