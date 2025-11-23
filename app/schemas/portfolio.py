from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.middleware.validation import sanitize_string, validate_url

# Schema untuk create portfolio
class PortfolioCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Portfolio title")
    description: Optional[str] = Field(None, max_length=2000, description="Portfolio description")
    category: str = Field(..., min_length=2, max_length=100, description="Portfolio category")
    image_url: str = Field(..., description="Image URL")
    published: bool = False
    order_index: int = Field(default=0, ge=0, description="Display order")
    
    @field_validator('title')
    @classmethod
    def sanitize_title(cls, v):
        return sanitize_string(v, max_length=255)
    
    @field_validator('description')
    @classmethod
    def sanitize_description(cls, v):
        if v:
            return sanitize_string(v, max_length=2000)
        return v
    
    @field_validator('category')
    @classmethod
    def sanitize_category(cls, v):
        return sanitize_string(v, max_length=100)
    
    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v):
        # Allow relative paths for uploaded files
        if v.startswith('/uploads/'):
            return v
        # Validate full URLs
        if not validate_url(v):
            raise ValueError('Invalid image URL format')
        return v

# Schema untuk update portfolio
class PortfolioUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    image_url: Optional[str] = None
    published: Optional[bool] = None
    order_index: Optional[int] = None

# Schema untuk response
class PortfolioResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    image_url: str
    published: bool
    order_index: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
