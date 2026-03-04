from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.models.schemas.session_schemas import (
    SessionCreate,
    SessionRead,
)
from app.api.sessions.genre import genre_router
from app.api.sessions.company import company_router
from app.api.sessions.system import system_router
from app.services import sessions


session_router = APIRouter(
    tags=["Sessions"],
)


@session_router.get(
    "/", response_model=List[SessionRead], summary="Получить все сессии"
)
async def read_all_sessions(session: AsyncSession = Depends(get_async_session)):
    result = await sessions.get_all_sessions(session)
    return result


@session_router.get(
    "session/{id}", response_model=SessionRead, summary="Получить сессию по ID"
)
async def read_session(id: int, session: AsyncSession = Depends(get_async_session)):
    return await sessions.get_session_by_id(session, id)


@session_router.post(
    "/",
    response_model=SessionCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сессию",
)
async def create_session(
    session_data: SessionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_session(session, session_data)


global_session_router = APIRouter(
    prefix="/sessions",
)


global_session_router.include_router(genre_router)
global_session_router.include_router(company_router)
global_session_router.include_router(system_router)
global_session_router.include_router(session_router)
