from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from sqlalchemy.orm import Session
from app.schemas.setting import Setting, SettingUpdate, SettingsPublic
from app.crud import setting as crud_setting
from app.utils.dependencies import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/public", response_model=SettingsPublic)
def get_public_settings(db: Session = Depends(get_db)):
    """
    Get all settings as key-value pairs (public endpoint)
    Used by frontend to display contact info, social media, etc.
    """
    return crud_setting.get_public_settings(db)


@router.get("/", response_model=List[Setting])
def get_all_settings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all settings with metadata (admin only)"""
    return crud_setting.get_all_settings(db)


@router.get("/category/{category}", response_model=List[Setting])
def get_settings_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get settings by category (admin only)"""
    return crud_setting.get_settings_by_category(db, category)


@router.get("/{key}", response_model=Setting)
def get_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get single setting by key (admin only)"""
    setting = crud_setting.get_setting_by_key(db, key)
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    return setting


@router.put("/{key}", response_model=Setting)
def update_setting(
    key: str,
    setting: SettingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update setting value (admin only)"""
    existing_setting = crud_setting.get_setting_by_key(db, key)
    if not existing_setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    return crud_setting.update_setting(db, key, setting)


@router.post("/bulk-update", status_code=status.HTTP_200_OK)
def bulk_update_settings(
    updates: Dict[str, str],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Bulk update multiple settings at once (admin only)
    Body: { "key1": "value1", "key2": "value2" }
    """
    crud_setting.bulk_update_settings(db, updates)
    return {"message": "Settings updated successfully", "count": len(updates)}
