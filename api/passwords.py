from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.passwords import PasswordEntryCreate, PasswordEntryUpdate, PasswordEntryOut, ResponseModel
from models.password_entry import PasswordEntry
from dependencies import get_db, get_current_user
from cryptography.fernet import Fernet
import os

router = APIRouter()
FERNET_KEY = os.getenv("FERNET_KEY", Fernet.generate_key())
fernet = Fernet(FERNET_KEY)

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

@router.get("/", response_model=ResponseModel)
def get_passwords(db: Session = Depends(get_db), user=Depends(get_current_user)):
    entries = db.query(PasswordEntry).filter(PasswordEntry.user_id == user.id).all()
    result = []
    for entry in entries:
        data = PasswordEntryOut.from_orm(entry).dict()
        data["password"] = decrypt_password(entry.password)
        result.append(data)
    return ResponseModel(success=True, message="Passwords fetched", data={"passwords": result})

@router.get("/{id}", response_model=ResponseModel)
def get_password(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    entry = db.query(PasswordEntry).filter(PasswordEntry.id == id, PasswordEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    data = PasswordEntryOut.from_orm(entry).dict()
    data["password"] = decrypt_password(entry.password)
    return ResponseModel(success=True, message="Password entry fetched", data={"password": data})

@router.post("/", response_model=ResponseModel)
def create_password(payload: PasswordEntryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    encrypted_pw = encrypt_password(payload.password)
    entry = PasswordEntry(user_id=user.id, title=payload.title, username=payload.username, password=encrypted_pw, url=payload.url, notes=payload.notes)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    data = PasswordEntryOut.from_orm(entry).dict()
    data["password"] = payload.password  # Show plaintext only on create
    return ResponseModel(success=True, message="Password entry created", data={"password": data})

@router.put("/{id}", response_model=ResponseModel)
def update_password(id: int, payload: PasswordEntryUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    entry = db.query(PasswordEntry).filter(PasswordEntry.id == id, PasswordEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    entry.title = payload.title
    entry.username = payload.username
    entry.password = encrypt_password(payload.password)
    entry.url = payload.url
    entry.notes = payload.notes
    db.commit()
    db.refresh(entry)
    data = PasswordEntryOut.from_orm(entry).dict()
    data["password"] = payload.password  # Show plaintext only on update
    return ResponseModel(success=True, message="Password entry updated", data={"password": data})

@router.delete("/{id}", response_model=ResponseModel)
def delete_password(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    entry = db.query(PasswordEntry).filter(PasswordEntry.id == id, PasswordEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return ResponseModel(success=True, message="Password entry deleted")

@router.get("/search", response_model=ResponseModel)
def search_passwords(q: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    entries = db.query(PasswordEntry).filter(
        PasswordEntry.user_id == user.id,
        (PasswordEntry.title.ilike(f"%{q}%")) | (PasswordEntry.username.ilike(f"%{q}%"))
    ).all()
    result = []
    for entry in entries:
        data = PasswordEntryOut.from_orm(entry).dict()
        data["password"] = decrypt_password(entry.password)
        result.append(data)
    return ResponseModel(success=True, message="Search results", data={"passwords": result})