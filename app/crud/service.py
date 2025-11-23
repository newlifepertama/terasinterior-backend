from app.schemas.service import ServiceCreate, ServiceUpdate
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException


def get_all_services(
    db: Session, 
    published_only: bool = False,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[dict], int]:
    """Get all services with pagination"""
    try:
        base_query = "FROM services"
        where_clause = " WHERE published = true" if published_only else ""
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}{where_clause}"
        total = db.execute(text(count_query)).scalar()
        
        # Get paginated items
        query = f"SELECT * {base_query}{where_clause} ORDER BY display_order LIMIT :limit OFFSET :skip"
        result = db.execute(text(query), {"limit": limit, "skip": skip})
        rows = result.fetchall()
        items = [dict(row._mapping) for row in rows]
        
        return items, total
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_service_by_id(db: Session, service_id: int) -> Optional[dict]:
    """Get service by ID"""
    try:
        result = db.execute(
            text("SELECT * FROM services WHERE id = :id"),
            {"id": service_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def create_service(db: Session, service: ServiceCreate) -> dict:
    """Create new service"""
    try:
        service_data = service.model_dump()
        result = db.execute(
            text("""
                INSERT INTO services (title, description, icon, features, display_order, published)
                VALUES (:title, :description, :icon, :features, :display_order, :published)
                RETURNING *
            """),
            service_data
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create service: {str(e)}")


def update_service(db: Session, service_id: int, service: ServiceUpdate) -> Optional[dict]:
    """Update service"""
    service_data = service.model_dump(exclude_unset=True)

    if not service_data:
        return get_service_by_id(db, service_id)

    try:
        set_clause = ", ".join([f"{key} = :{key}" for key in service_data.keys()])
        query = f"UPDATE services SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = :id RETURNING *"
        
        result = db.execute(
            text(query),
            {**service_data, "id": service_id}
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update service: {str(e)}")


def delete_service(db: Session, service_id: int) -> bool:
    """Delete service"""
    try:
        result = db.execute(
            text("DELETE FROM services WHERE id = :id RETURNING id"),
            {"id": service_id}
        )
        db.commit()
        return result.fetchone() is not None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete service: {str(e)}")
