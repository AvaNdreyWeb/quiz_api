from datetime import datetime

from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int
    answer_text: str
    question_text: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostQuestionsNum(BaseModel):
    questions_num: int = Field(gt=0)
