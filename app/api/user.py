from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.models.schemas.user_schemas import UserCreate, UserRead

from app.services import user


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    return await user.create_user(session, user_data)


@router.get(
    "/",
    response_model=List[UserRead],
    summary="get all users"
)
async def get_all_user(session: AsyncSession = Depends(get_async_session)):
    return await user.get_all_users(session)