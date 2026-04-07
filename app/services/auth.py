from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import config
from app.models.orm.models import User

def create_access_token(user: User) -> str:
    """Создает access token с данными пользователя"""
    to_encode = {
        "sub": str(user.id),
        "login": user.login,
        "role": user.role,  
        "type": "access"
    }
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def create_refresh_token(user: User) -> str:
    """Refresh token содержит минимум данных"""
    to_encode = {
        "sub": str(user.id),
        "type": "refresh"
    }
    expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return payload
    except JWTError:
        return None