from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema untuk login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema untuk user response
class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str
    
    class Config:
        from_attributes = True

# Schema untuk token response
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
