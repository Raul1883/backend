from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import ForeignKeyViolationError
from app.models.orm.models import Company, Genre, System
from app.models.schemas.session_schemas import (
    CompanySchema,
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
    prefix="/sessions",
    tags=["Sessions"],
)

# Sessions


@router.get("/", response_model=List[SessionRead], summary="Получить все сессии")
async def read_all_sessions(session: AsyncSession = Depends(get_async_session)):
    result = await sessions.get_all_sessions(session)
    return result


@router.get(
    "session/{user_id}", response_model=UserRead, summary="Получить сессию по ID"
)
async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_orm = await user.get_user_by_id(session, user_id)

    await raise_404_if_none(user_orm, user_id)

    return user_orm


@router.post(
    "/",
    response_model=SessionCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сессию",
)
async def create_session(
    session_data: SessionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_session_orm = await sessions.create_session(session, session_data)
        return new_session_orm

    except ForeignKeyViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# Sessions attributes
# Genre
@router.post(
    "/genre",
    response_model=GenreSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_genre(
    genre_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, Genre, {"text": genre_name})


@router.get("/genre", response_model=List[GenreSchema], status_code=status.HTTP_200_OK)
async def get_all_genres(
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_all_attributes(session, Genre)


@router.get(
    "/genre/{genre_id}", response_model=GenreSchema, status_code=status.HTTP_200_OK
)
async def get_genre_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, Genre, id)


@router.delete("/genre/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, Genre, id)


# System
@router.post(
    "/system",
    response_model=SystemSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_system(
    system_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, System, {"text": system_name})


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
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, System, id)


@router.delete("/system/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, System, id)


# Company
@router.post(
    "/company",
    response_model=CompanySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    company_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, Company, {"title": company_name})


@router.get(
    "/company", response_model=List[CompanySchema], status_code=status.HTTP_200_OK
)
async def get_all_companies(
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_all_attributes(session, Company)


@router.get(
    "/company/{company_id}",
    response_model=CompanySchema,
    status_code=status.HTTP_200_OK,
)
async def get_company_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, Company, id)


@router.delete("/company/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, Company, id)


# Utils


async def raise_404_if_none(obj, session_id):
    """deprecated"""
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session{session_id} not found",
        )
