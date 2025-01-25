# app/schemas/auth.py
from pydantic import BaseModel, EmailStr

# Schema for login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Schema for login response
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
