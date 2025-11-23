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
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login with email and password - bcrypt verification"""
    try:
        # Get user from PostgreSQL
        user = db.execute(
            text("SELECT id, email, password_hash, name, role FROM users WHERE email = :email"),
            {"email": login_data.email}
        ).fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Email atau password salah")
        
        # Verify password with bcrypt
        is_valid = bcrypt.checkpw(
            login_data.password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        )
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Email atau password salah")
        
        # Generate JWT token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        }
        access_token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan server")

@router.get("/me")
async def get_current_user():
    """Get current user info"""
    return {"message": "Get current user endpoint"}
