from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.services.auth_service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(db, user.email, user.password)

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await AuthService.login(db, user.email, user.password)
    return {"access_token": token}