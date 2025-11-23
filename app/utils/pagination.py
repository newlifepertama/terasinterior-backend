"""Pagination utilities"""
from typing import TypeVar, Generic, List
from pydantic import BaseModel
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Pagination query parameters"""
    page: int = 1
    page_size: int = 10
    
    def get_offset(self) -> int:
        """Calculate offset for SQL query"""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get limit for SQL query"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """Create paginated response"""
        total_pages = ceil(total / page_size) if page_size > 0 else 0
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
