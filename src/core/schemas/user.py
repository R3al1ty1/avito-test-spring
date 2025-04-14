from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    role: str
    
class UserCreate(UserBase):
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(UserBase):
    id: UUID
    
class DummyLogin(BaseModel):
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str