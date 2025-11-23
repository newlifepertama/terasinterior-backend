from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from app.schemas.service import Service, ServiceCreate, ServiceUpdate
from app.crud import service as crud_service
from app.utils.dependencies import get_current_user
from app.database import get_db
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("/", response_model=PaginatedResponse[Service])
def get_services(
    published_only: bool = True,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all services (public endpoint) with pagination
    - published_only: Filter only published services (default: True)
    """
    skip = (page - 1) * page_size
    items, total = crud_service.get_all_services(db, published_only, skip=skip, limit=page_size)
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.get("/{service_id}", response_model=Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get service by ID"""
    service = crud_service.get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new service (admin only)"""
    return crud_service.create_service(db, service)


@router.put("/{service_id}", response_model=Service)
def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update service (admin only)"""
    updated_service = crud_service.update_service(db, service_id, service)
    if not updated_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return updated_service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete service (admin only)"""
    success = crud_service.delete_service(db, service_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return None
