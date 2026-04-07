from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.dependencies.auth import AnyUser, MasterUser, PlayerUser
from app.models.schemas.session_schemas import (
    SessionCreate,
    SessionRead,
    SessionUpdate,
)
from app.api.sessions.genre import router
from app.api.sessions.company import router
from app.api.sessions.system import router
from app.services import sessions


router = APIRouter(tags=["Sessions"], prefix="/sessions")


@router.get("", response_model=List[SessionRead], summary="Получить все сессии")
async def read_all_sessions(session: AsyncSession = Depends(get_async_session)):
    result = await sessions.get_all_sessions(session)
    return result


@router.get("/{id}", response_model=SessionRead, summary="Получить сессию по ID")
async def read_session(
    id: int,
    current_user: AnyUser,
    session: AsyncSession = Depends(get_async_session),
    
):
    return await sessions.get_session_by_id(session, id)


@router.post(
    "",
    response_model=SessionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сессию",
)
async def create_session(
    session_data: SessionCreate,
    session: AsyncSession = Depends(get_async_session),
):

    res = await sessions.create_session(session, session_data)

    return res


@router.patch(
    "/{id}",
    response_model=SessionRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить сессию",
)
async def update_session(
    id: int,
    session_data: SessionUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.update_session(session, id, session_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_session(session, id)
