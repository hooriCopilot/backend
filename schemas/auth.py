from pydantic import BaseModel, EmailStr, constr

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: dict = None
    errors: list = []