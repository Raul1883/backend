from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session
from app.models.orm.models import User
from app.models.schemas.user_schemas import (
    LoginRequest,
    LoginResponse,
    Token,
    UserCreate,
    UserRead,
)
from app.services.user import (
    authenticate_user,
    create_user,
    get_user_by_id,
    get_user_by_login,
)
from app.services.auth import create_access_token, create_refresh_token, verify_token
from app.services.refresh_token import (
    create_refresh_token_record,
    get_valid_refresh_token,
    revoke_refresh_token,
)
from app.dependencies.auth import get_current_user
from app.config import config

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    user = await authenticate_user(session, login_data.login, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    # Создаем токены с ролью пользователя
    access_token = create_access_token(user)  # 👈 Передаем весь объект user
    refresh_token = create_refresh_token(user)

    # Сохраняем refresh token в БД с fingerprint
    user_agent = request.headers.get("user-agent")
    client_ip = request.client.host if request.client else None

    await create_refresh_token_record(
        session, user.id, refresh_token, user_agent, client_ip
    )

    # Устанавливаем refresh token в httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=config.COOKIE_HTTPONLY,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return LoginResponse(
        access_token=access_token,
        user=UserRead.model_validate(user),  # 👈 Роль уже здесь
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    
    stored_token = await get_valid_refresh_token(session, refresh_token)
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token",
        )
    
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user = await get_user_by_id(session, int(payload["sub"]))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(user)

    return Token(access_token=new_access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),  # опционально, для логирования
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await revoke_refresh_token(session, refresh_token)

    response.delete_cookie("refresh_token")
    return


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    existing = await get_user_by_login(session, user_data.login)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    return await create_user(session, user_data)
