"""File upload utilities"""
import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
import imghdr

# Upload directory
UPLOAD_DIR = Path("uploads/portfolio")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed image types
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_image(file: UploadFile) -> Tuple[bool, str]:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file extension
    if not file.filename:
        return False, "No filename provided"
    
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    return True, ""


async def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to local storage
    
    Args:
        file: Uploaded file
        
    Returns:
        Relative file path
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file
    is_valid, error = validate_image(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Verify it's actually an image
    image_type = imghdr.what(None, content)
    if not image_type:
        raise HTTPException(status_code=400, detail="File is not a valid image")
    
    # Generate unique filename
    ext = file.filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Return relative path for URL
    return f"/uploads/portfolio/{filename}"


def delete_upload_file(file_path: str) -> bool:
    """
    Delete uploaded file
    
    Args:
        file_path: Relative file path (e.g., /uploads/portfolio/xxx.jpg)
        
    Returns:
        True if deleted, False if file not found
    """
    try:
        # Remove leading slash and construct full path
        relative_path = file_path.lstrip('/')
        full_path = Path(relative_path)
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception:
        return False
