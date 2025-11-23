from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SettingBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)
    category: str = Field(..., min_length=1, max_length=50)
    label: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    input_type: str = Field(default="text", max_length=20)


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    value: str = Field(...)


class Setting(SettingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SettingsPublic(BaseModel):
    """Public settings response (key-value pairs only)"""
    contact_phone: Optional[str] = None
    contact_whatsapp: Optional[str] = None
    contact_email: Optional[str] = None
    contact_address: Optional[str] = None
    company_name: Optional[str] = None
    company_tagline: Optional[str] = None
    company_description: Optional[str] = None
    social_instagram: Optional[str] = None
    social_facebook: Optional[str] = None
    social_youtube: Optional[str] = None
    social_tiktok: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    hours_weekday: Optional[str] = None
    hours_weekend: Optional[str] = None
