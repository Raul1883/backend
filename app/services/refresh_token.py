from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models.orm.models import RefreshToken
from app.services.auth import create_refresh_token, verify_token

async def create_refresh_token_record(
    session: AsyncSession,
    user_id: int,
    token: str,
    user_agent: str | None = None,
    ip_address: str | None = None
) -> RefreshToken:
    """Сохранить refresh token в БД"""
    payload = verify_token(token)
    if not payload:
        raise ValueError("Invalid token")
    
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=datetime.fromtimestamp(payload["exp"]),
        user_agent=user_agent,
        ip_address=ip_address
    )
    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)
    return refresh_token

async def get_valid_refresh_token(
    session: AsyncSession,
    token: str
) -> RefreshToken | None:
    """Проверить refresh token в БД"""
    result = await session.execute(
        select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
    )
    return result.scalar_one_or_none()

async def revoke_refresh_token(session: AsyncSession, token: str):
    """Отозвать refresh token"""
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    refresh_token = result.scalar_one_or_none()
    if refresh_token:
        refresh_token.revoked = True
        await session.commit()

async def revoke_all_user_tokens(session: AsyncSession, user_id: int):
    """Отозвать все токены пользователя (при смене пароля)"""
    await session.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .values(revoked=True)
    )
    await session.commit()