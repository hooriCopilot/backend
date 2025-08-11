from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class PasswordEntry(Base):
    __tablename__ = "password_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    username = Column(String(100))
    password = Column(String(256), nullable=False)  # encrypted
    url = Column(String(200))
    notes = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())