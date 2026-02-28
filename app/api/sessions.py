from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.models.schemas.session_schemas import SessionRead
from app.models.schemas.user_schemas import UserRead, UserCreate

from app.services import user
from app.services import sessions

router = APIRouter(
    prefix="/sessions",
    tags=["Quests"],
)

@router.get("/", response_model=List[SessionRead], summary="Получить все сессии")
async def read_all_sessions(session:AsyncSession= Depends(get_async_session)):
    return await sessions.get_all_sessions(session)


@router.get("/{user_id}", response_model=UserRead, summary="Получить user по ID")
async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_orm = await user.get_user_by_id(session, user_id)

    await raise_404_if_none(user_orm, user_id)

    return user_orm


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать user",
)
async def create_quest(
    user_data: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_user_orm = await user.create_user(session, user_data)
    except user.UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    
    return new_user_orm


async def raise_404_if_none(obj, session_id):
    """deprecated"""
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session{session_id} not found",
        )
