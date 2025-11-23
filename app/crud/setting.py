from app.schemas.setting import SettingUpdate
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException


def get_all_settings(db: Session) -> List[dict]:
    """Get all settings"""
    try:
        result = db.execute(text("SELECT * FROM settings ORDER BY category, key"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_settings_by_category(db: Session, category: str) -> List[dict]:
    """Get settings by category"""
    try:
        result = db.execute(
            text("SELECT * FROM settings WHERE category = :category ORDER BY key"),
            {"category": category}
        )
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_setting_by_key(db: Session, key: str) -> Optional[dict]:
    """Get setting by key"""
    try:
        result = db.execute(
            text("SELECT * FROM settings WHERE key = :key"),
            {"key": key}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_public_settings(db: Session) -> Dict[str, str]:
    """Get all settings as key-value pairs for public use"""
    try:
        result = db.execute(text("SELECT key, value FROM settings"))
        rows = result.fetchall()
        return {row.key: row.value for row in rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def update_setting(db: Session, key: str, setting: SettingUpdate) -> dict:
    """Update setting value"""
    try:
        result = db.execute(
            text("""
                UPDATE settings 
                SET value = :value, updated_at = CURRENT_TIMESTAMP 
                WHERE key = :key 
                RETURNING *
            """),
            {"value": setting.value, "key": key}
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update setting: {str(e)}")


def bulk_update_settings(db: Session, updates: Dict[str, str]) -> bool:
    """Update multiple settings at once"""
    try:
        for key, value in updates.items():
            db.execute(
                text("UPDATE settings SET value = :value, updated_at = CURRENT_TIMESTAMP WHERE key = :key"),
                {"value": value, "key": key}
            )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to bulk update settings: {str(e)}")
