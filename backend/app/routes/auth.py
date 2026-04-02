from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db  # async session generator
from app.models.user import User
from app.schema.schemas import UserCreate
from app.utils.auth import hash_password, verify_password, create_token, verify_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])

# OAuth2 for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# JWT-protected route
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = create_token.verify_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    result = await db.execute(select(User).filter(User.id == payload["user_id"]))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


# Role-based access
def require_role(role: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return current_user
    return role_checker


# Register
@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, password=hash_password(user.password), role="user")
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}


# Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_token({"user_id": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}


# Profile
@router.get("/profile")
async def profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


# Admin-only route
admin_only = require_role("admin")

@router.get("/admin-dashboard")
async def admin_dashboard(current_user: User = Depends(admin_only)):
    return {"message": "Welcome Admin!", "user": current_user.email}