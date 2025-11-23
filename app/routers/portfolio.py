from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioResponse
from app.crud import portfolio as crud
from app.utils.dependencies import get_current_user
from app.database import get_db
from app.utils.pagination import PaginatedResponse
from app.utils.file_upload import save_upload_file, delete_upload_file

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])

# Public endpoint - get published portfolio
@router.get("/", response_model=PaginatedResponse[PortfolioResponse])
def get_portfolio(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get all published portfolio items with pagination"""
    skip = (page - 1) * page_size
    items, total = crud.get_all_portfolio(db, published_only=True, skip=skip, limit=page_size)
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)

# Admin endpoint - get all portfolio
@router.get("/admin", response_model=PaginatedResponse[PortfolioResponse])
def get_all_portfolio_admin(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all portfolio items (admin only) with pagination"""
    skip = (page - 1) * page_size
    items, total = crud.get_all_portfolio(db, published_only=False, skip=skip, limit=page_size)
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)

# Get single portfolio
@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio_by_id(portfolio_id: int, db: Session = Depends(get_db)):
    """Get portfolio item by ID"""
    portfolio = crud.get_portfolio_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

# Create portfolio (admin only)
@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new portfolio item (admin only)"""
    return crud.create_portfolio(db, portfolio)

# Update portfolio (admin only)
@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: int,
    portfolio: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update portfolio item (admin only)"""
    updated = crud.update_portfolio(db, portfolio_id, portfolio)
    if not updated:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return updated

# Delete portfolio (admin only)
@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete portfolio item (admin only)"""
    # Get portfolio to delete image file
    portfolio = crud.get_portfolio_by_id(db, portfolio_id)
    if portfolio and portfolio.get('image_url', '').startswith('/uploads/'):
        delete_upload_file(portfolio['image_url'])
    
    success = crud.delete_portfolio(db, portfolio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return None

# Upload image (admin only)
@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Upload portfolio image (admin only)"""
    try:
        file_path = await save_upload_file(file)
        return {
            "url": file_path,
            "filename": file.filename,
            "message": "Image uploaded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
