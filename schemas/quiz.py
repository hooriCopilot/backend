from pydantic import BaseModel
from typing import List, Dict, Any

class QuizSubmitRequest(BaseModel):
    answers: List[Dict[str, Any]]

class QuizResult(BaseModel):
    id: int
    results: Dict[str, Any]
    completed_at: str

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: dict = None
    errors: list = []