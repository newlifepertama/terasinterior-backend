"""Request validation middleware"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import html

# Request size limit (10MB)
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB in bytes

class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size"""
    
    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                content_length = int(content_length)
                if content_length > MAX_REQUEST_SIZE:
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Request body too large. Maximum size is {MAX_REQUEST_SIZE / (1024*1024)}MB"
                        }
                    )
            except ValueError:
                pass
        
        response = await call_next(request)
        return response


def sanitize_string(value: str, max_length: int = None) -> str:
    """
    Sanitize string input to prevent XSS and injection attacks
    
    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not value:
        return value
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Escape HTML to prevent XSS
    value = html.escape(value)
    
    # Limit length if specified
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate Indonesian phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    # Indonesian phone: 08xx-xxxx-xxxx or +62xxx
    pattern = r'^(\+62|62|0)[0-9]{9,12}$'
    # Remove spaces and dashes
    phone_clean = phone.replace(' ', '').replace('-', '')
    return bool(re.match(pattern, phone_clean))


def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))
