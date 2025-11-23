from typing import List, Optional
from app.schemas.contact import ContactCreate, ContactUpdate
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

def get_all_contacts(db: Session) -> List[dict]:
    """Get all contact submissions"""
    try:
        result = db.execute(text("SELECT * FROM contacts ORDER BY created_at DESC"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_contact_by_id(db: Session, contact_id: int) -> Optional[dict]:
    """Get single contact"""
    try:
        result = db.execute(
            text("SELECT * FROM contacts WHERE id = :id"),
            {"id": contact_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def create_contact(db: Session, contact: ContactCreate) -> dict:
    """Create new contact submission"""
    try:
        result = db.execute(
            text("""
                INSERT INTO contacts (name, email, phone, message, status)
                VALUES (:name, :email, :phone, :message, 'new')
                RETURNING *
            """),
            contact.dict()
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create contact: {str(e)}")

def update_contact_status(db: Session, contact_id: int, status: str) -> Optional[dict]:
    """Update contact status"""
    try:
        result = db.execute(
            text("""
                UPDATE contacts 
                SET status = :status, updated_at = CURRENT_TIMESTAMP 
                WHERE id = :id 
                RETURNING *
            """),
            {"status": status, "id": contact_id}
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update contact: {str(e)}")

def delete_contact(db: Session, contact_id: int) -> bool:
    """Delete contact"""
    try:
        result = db.execute(
            text("DELETE FROM contacts WHERE id = :id RETURNING id"),
            {"id": contact_id}
        )
        db.commit()
        return result.fetchone() is not None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete contact: {str(e)}")
