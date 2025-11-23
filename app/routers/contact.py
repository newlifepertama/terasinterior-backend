from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from sqlalchemy.orm import Session
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from app.crud import contact as crud
from app.utils.dependencies import get_current_user
from app.database import get_db
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/api/contact", tags=["Contact"])

# Public endpoint - submit contact form
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")  # Max 3 contact submissions per hour
def submit_contact(request: Request, contact: ContactCreate, db: Session = Depends(get_db)):
    """Submit contact form (public endpoint)"""
    return crud.create_contact(db, contact)

# Admin endpoint - get all contacts
@router.get("/", response_model=List[ContactResponse])
def get_all_contacts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all contact submissions (admin only)"""
    return crud.get_all_contacts(db)

# Admin endpoint - get single contact
@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get contact by ID (admin only)"""
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Admin endpoint - update contact status
@router.patch("/{contact_id}/status", response_model=ContactResponse)
def update_contact_status(
    contact_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update contact status (admin only)"""
    updated = crud.update_contact_status(db, contact_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated

# Admin endpoint - delete contact
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete contact (admin only)"""
    success = crud.delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None
