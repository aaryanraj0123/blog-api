from datetime import datetime, timedelta, timezone
from jose import jwt 
from argon2 import PasswordHasher

from app.core.config import get_settings

settings = get_settings()

pwd_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try: 
        return pwd_hasher.verify(hashed_password, plain_password)
    except Exception:
        return False 
    
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm,)
