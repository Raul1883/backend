from fastapi import APIRouter, Depends, status
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.models.orm.models import Genre
from app.models.schemas.session_schemas import (
    GenreSchema, CreateGenreSchema
)

from app.services import sessions

router = APIRouter(
    tags=["Genre"],
)


@router.post(
    "/genre",
    response_model=GenreSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_genre(
    genre: CreateGenreSchema,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.create_attribute(session, Genre, genre)


@router.get(
    "/genre", response_model=List[GenreSchema], status_code=status.HTTP_200_OK
)
async def get_all_genres(
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_all_attributes(session, Genre)



@router.get(
    "/genre/{genre_id}", response_model=GenreSchema, status_code=status.HTTP_200_OK
)
async def get_genre_by_id(
    genre_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await sessions.get_attribute_by_id(session, Genre, genre_id)


@router.delete("/genre/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genre_id: int, session: AsyncSession = Depends(get_async_session)):
    await sessions.delete_attribute(session, Genre, genre_id)
