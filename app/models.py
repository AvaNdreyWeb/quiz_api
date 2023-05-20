from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, unique=True)
    answer_text = Column(String)
    question_text = Column(String)
    created_at = Column(DateTime)
