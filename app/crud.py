from fastapi import status
from sqlalchemy.orm import Session

from . import models, schemas


def get_question_by_id(db: Session, id: int):
    db_question = db.query(models.Question).filter(
        models.Question.id == id
    ).first()
    return db_question


def create_question(db: Session, question: schemas.Question):
    new_question = models.Question(**question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return status.HTTP_201_CREATED


def get_last_question(db: Session):
    db_questions = db.query(models.Question).all()
    if db_questions:
        return db_questions[-1]
    return {}
