from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ServiceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    icon: str = Field(..., min_length=1, max_length=50)
    features: List[str] = Field(default_factory=list)
    display_order: int = Field(default=0, ge=0)
    published: bool = Field(default=True)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    icon: Optional[str] = Field(None, min_length=1, max_length=50)
    features: Optional[List[str]] = None
    display_order: Optional[int] = Field(None, ge=0)
    published: Optional[bool] = None


class Service(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
