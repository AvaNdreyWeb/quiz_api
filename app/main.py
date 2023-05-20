from datetime import datetime
from typing import Dict, Union

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, database, schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
client = httpx.AsyncClient()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_question():
    response = await client.get("https://jservice.io/api/random?count=1")
    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
    return response.json()[0]


async def get_questions_list(num: int):
    response = await client.get(f"https://jservice.io/api/random?count={num}")
    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
    return response.json()


@app.get("/")
def documentation_link():
    return {"documentation": "http://127.0.0.1:8000/docs"}


@app.post("/questions", response_model=Union[schemas.Question, Dict])
async def create_questions(
    data: schemas.PostQuestionsNum,
    db: Session = Depends(get_db)
):
    last_question = crud.get_last_question(db)
    questions_list = await get_questions_list(data.questions_num)

    for question in questions_list:
        while crud.get_question_by_id(db, question["id"]):
            question = await get_question()

        new_question = schemas.Question(
            id=question["id"],
            answer_text=question["answer"],
            question_text=question["question"],
            created_at=datetime.strptime(
                question["created_at"],
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        )
        crud.create_question(db, new_question)

    if last_question:
        return last_question
    return {}
