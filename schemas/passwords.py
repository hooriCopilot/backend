from pydantic import BaseModel, Field
from typing import Optional

class PasswordEntryBase(BaseModel):
    title: str
    username: Optional[str]
    password: str
    url: Optional[str]
    notes: Optional[str]

class PasswordEntryCreate(PasswordEntryBase):
    pass

class PasswordEntryUpdate(PasswordEntryBase):
    pass

class PasswordEntryOut(PasswordEntryBase):
    id: int
    class Config:
        orm_mode = True

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: dict = None
    errors: list = []