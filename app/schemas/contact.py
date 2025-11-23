from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.middleware.validation import sanitize_string, validate_phone

# Schema untuk create contact
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Contact name")
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    message: str = Field(..., min_length=10, max_length=2000, description="Message content")
    
    @field_validator('name')
    @classmethod
    def sanitize_name(cls, v):
        return sanitize_string(v, max_length=255)
    
    @field_validator('message')
    @classmethod
    def sanitize_message(cls, v):
        return sanitize_string(v, max_length=2000)
    
    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Invalid phone number format')
        return v

# Schema untuk update contact
class ContactUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)

# Schema untuk response
class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    message: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
