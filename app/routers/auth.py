from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr
import bcrypt
from datetime import datetime, timedelta
import jwt
from app.config import settings
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str  # Bisa username atau email
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login with username/email and password - bcrypt verification"""
    try:
        # Get user from PostgreSQL (support both username and email)
        user = db.execute(
            text("""
                SELECT id, username, email, hashed_password, is_active 
                FROM admin_users 
                WHERE username = :username OR email = :username
            """),
            {"username": login_data.username}
        ).fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Username atau password salah")
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Akun tidak aktif")
        
        # Verify password with bcrypt
        is_valid = bcrypt.checkpw(
            login_data.password.encode('utf-8'),
            user.hashed_password.encode('utf-8')
        )
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Username atau password salah")
        
        # Generate JWT token
        token_data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        }
        access_token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan server: {str(e)}")

@router.get("/me")
async def get_current_user():
    """Get current user info"""
    return {"message": "Get current user endpoint"}
