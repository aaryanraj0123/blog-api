from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:

    @staticmethod
    async def register(db: AsyncSession, email: str, password: str):
        existing = await UserRepository.get_by_email(db, email)
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        
        user = User(
            email=email,
            password_hash=hash_password(password),
            role="AUTHOR",
        )

        return await UserRepository.create(db, user)
    
    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        user = await UserRepository.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return create_access_token(
            {"sub": str(user.id), "role": user.role.value}
        )