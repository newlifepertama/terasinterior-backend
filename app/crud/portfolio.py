from typing import List, Optional, Tuple
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

def get_all_portfolio(
    db: Session, 
    published_only: bool = False,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[dict], int]:
    """
    Get all portfolio items with pagination
    
    Returns:
        Tuple of (items, total_count)
    """
    try:
        # Build base query
        base_query = "FROM portfolio"
        where_clause = " WHERE published = true" if published_only else ""
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}{where_clause}"
        total = db.execute(text(count_query)).scalar()
        
        # Get paginated items
        query = f"SELECT * {base_query}{where_clause} ORDER BY order_index, created_at DESC LIMIT :limit OFFSET :skip"
        result = db.execute(text(query), {"limit": limit, "skip": skip})
        rows = result.fetchall()
        items = [dict(row._mapping) for row in rows]
        
        return items, total
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_portfolio_by_id(db: Session, portfolio_id: int) -> Optional[dict]:
    """Get single portfolio item"""
    try:
        result = db.execute(
            text("SELECT * FROM portfolio WHERE id = :id"),
            {"id": portfolio_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def create_portfolio(db: Session, portfolio: PortfolioCreate) -> dict:
    """Create new portfolio item"""
    try:
        result = db.execute(
            text("""
                INSERT INTO portfolio (title, description, category, image_url, published, order_index)
                VALUES (:title, :description, :category, :image_url, :published, :order_index)
                RETURNING *
            """),
            portfolio.dict()
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create portfolio: {str(e)}")

def update_portfolio(db: Session, portfolio_id: int, portfolio: PortfolioUpdate) -> Optional[dict]:
    """Update portfolio item"""
    update_data = portfolio.dict(exclude_unset=True)
    
    if not update_data:
        return get_portfolio_by_id(db, portfolio_id)
    
    try:
        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = f"UPDATE portfolio SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = :id RETURNING *"
        
        result = db.execute(
            text(query),
            {**update_data, "id": portfolio_id}
        )
        db.commit()
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update portfolio: {str(e)}")

def delete_portfolio(db: Session, portfolio_id: int) -> bool:
    """Delete portfolio item"""
    try:
        result = db.execute(
            text("DELETE FROM portfolio WHERE id = :id RETURNING id"),
            {"id": portfolio_id}
        )
        db.commit()
        return result.fetchone() is not None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete portfolio: {str(e)}")
