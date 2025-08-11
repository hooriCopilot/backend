from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.quiz import QuizSubmitRequest, QuizResult, ResponseModel
from models.quiz_submission import QuizSubmission
from dependencies import get_db, get_current_user
from datetime import datetime

router = APIRouter()

CAREERS = [
    {
        "name": "UI/UX Designer",
        "title": "UI/UX Designer",
        "match": 70,
        "description": "Design user-friendly digital experiences.",
        "skills": ["Wireframing", "Figma", "User Research"],
        "resources": [
            {"title": "UI Design Basics", "url": "https://example.com/ui", "type": "course"}
        ]
    },
    {
        "name": "Cybersecurity Analyst",
        "title": "Cybersecurity Analyst",
        "match": 65,
        "description": "Protect systems and data from threats.",
        "skills": ["Network Security", "Python", "Analysis"],
        "resources": [
            {"title": "Intro to Cybersecurity", "url": "https://example.com/cyber", "type": "course"}
        ]
    },
    {
        "name": "Data Scientist",
        "title": "Data Scientist",
        "match": 80,
        "description": "Analyze and interpret complex data to drive decision-making.",
        "skills": ["Python", "Statistics", "Machine Learning"],
        "resources": [
            {"title": "Data Science Bootcamp", "url": "https://example.com/ds", "type": "course"}
        ]
    },
    {
        "name": "Software Engineer",
        "title": "Software Engineer",
        "match": 90,
        "description": "Design, develop, and maintain software systems.",
        "skills": ["JavaScript", "React", "Node.js", "System Design"],
        "resources": [
            {"title": "JavaScript Mastery", "url": "https://example.com/js", "type": "course"}
        ]
    }
    # Add even more careers here!
]

def score_careers(answers):
    scores = {career["name"]: 0 for career in CAREERS}
    for answer in answers:
        text = (answer.get("answer") or "").lower()
        for career in CAREERS:
            for skill in career["skills"]:
                if skill in text:
                    scores[career["name"]] += 1
    sorted_careers = sorted(CAREERS, key=lambda c: scores[c["name"]], reverse=True)
    return [{"career": c, "score": scores[c["name"]]} for c in sorted_careers[:3]]

@router.post("/submit", response_model=ResponseModel)
def submit_quiz(payload: QuizSubmitRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    results = score_careers(payload.answers)
    submission = QuizSubmission(user_id=user.id, answers=payload.answers, completed_at=datetime.utcnow(), results=results)
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return ResponseModel(success=True, message="Quiz submitted", data={"results": results, "id": submission.id})

@router.get("/history", response_model=ResponseModel)
def quiz_history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    subs = db.query(QuizSubmission).filter(QuizSubmission.user_id == user.id).all()
    data = [
        {"id": s.id, "completed_at": s.completed_at, "results": s.results}
        for s in subs
    ]
    return ResponseModel(success=True, message="Quiz history fetched", data={"history": data})

@router.get("/results/{id}", response_model=ResponseModel)
def quiz_result(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = db.query(QuizSubmission).filter(QuizSubmission.id == id, QuizSubmission.user_id == user.id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResponseModel(success=True, message="Result fetched", data={"result": s.results})