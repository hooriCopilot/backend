from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    answers = Column(JSON, nullable=False)
    completed_at = Column(DateTime, server_default=func.now())
    results = Column(JSON, nullable=True)