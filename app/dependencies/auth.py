from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session
from app.models.orm.models import User
from app.services.auth import verify_token
from app.services.user import get_user_by_id

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    user = await get_user_by_id(session, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    # Здесь можно добавить проверки: is_active, is_verified и т.д.
    return current_user


async def get_current_user_role(
    current_user: User = Depends(get_current_user)
) -> str:
    """Получить роль текущего пользователя"""
    return current_user.role

# Создаем зависимости для проверки ролей
def require_role(required_role: str):
    """Фабрика зависимостей для проверки конкретной роли"""
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        return current_user
    return role_checker

def require_any_role(*allowed_roles: str):
    """Проверка на любую из разрешенных ролей"""
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


AnyUser = Annotated[User, Depends(get_current_user)]
MasterUser = Annotated[User, Depends(require_role("master"))]
PlayerUser = Annotated[User, Depends(require_role("player"))]
