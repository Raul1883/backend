from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import ForeignKeyViolationError
from app.models.orm.models import Company, Genre, System
from app.models.schemas.session_schemas import (
    CompanySchema,
    CreateSystemSchema,
    GenreSchema,
    SessionCreate,
    SessionRead,
    SystemSchema,
)
from app.models.schemas.user_schemas import UserRead, UserCreate

from app.services import user
from app.services import sessions
from app.exceptions.service_exceptions import AttributeAlreadyExistsError


router = APIRouter(
    tags=["System"],
)


@router.post(
    "/system",
    response_model=SystemSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_system(
    system: CreateSystemSchema,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, System, system)


@router.get(
    "/system", response_model=List[SystemSchema], status_code=status.HTTP_200_OK
)
async def get_all_systems(
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_all_attributes(session, System)


@router.get(
    "/system/{system_id}", response_model=SystemSchema, status_code=status.HTTP_200_OK
)
async def get_system_by_id(
    system_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, System, system_id)


@router.delete("/system/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(system_id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, System, system_id)
