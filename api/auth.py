from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from schemas.auth import RegisterRequest, LoginRequest, Token, UserProfile, ResponseModel
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from dependencies import get_db, get_current_user
from core.logger import logger

router = APIRouter()

@router.post("/register", response_model=ResponseModel)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        return ResponseModel(success=False, message="Email already registered", errors=["Email exists"])
    user = User(name=payload.name, email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return ResponseModel(success=True, message="Registered successfully", data={"user": {"id": user.id, "name": user.name, "email": user.email}})

@router.post("/login", response_model=ResponseModel)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return ResponseModel(success=True, message="Login successful", data={"access_token": token})

@router.post("/logout", response_model=ResponseModel)
def logout():
    # Token invalidation handled on client side (stateless JWT)
    return ResponseModel(success=True, message="Logged out successfully")

@router.get("/profile", response_model=ResponseModel)
def profile(current_user: User = Depends(get_current_user)):
    return ResponseModel(success=True, message="Profile fetched", data={"user": {"id": current_user.id, "name": current_user.name, "email": current_user.email}})