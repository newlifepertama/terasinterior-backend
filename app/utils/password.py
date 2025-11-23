"""Password validation and security utilities"""
import re
from typing import Tuple

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def check_common_passwords(password: str) -> bool:
    """
    Check if password is in common passwords list
    
    Args:
        password: Password to check
        
    Returns:
        True if password is common (weak), False otherwise
    """
    common_passwords = [
        'password', '12345678', 'qwerty', 'abc123', 'monkey',
        'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou',
        'master', 'sunshine', 'ashley', 'bailey', 'passw0rd',
        'shadow', '123123', '654321', 'superman', 'qazwsx',
        'admin', 'admin123', 'password123', 'welcome', 'login'
    ]
    
    return password.lower() in common_passwords


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Complete password validation
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check strength
    is_strong, error = validate_password_strength(password)
    if not is_strong:
        return False, error
    
    # Check common passwords
    if check_common_passwords(password):
        return False, "Password is too common. Please choose a stronger password"
    
    return True, ""
