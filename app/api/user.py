from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.dependencies.auth import get_current_user
from app.models.orm.models import User
from app.models.schemas.user_schemas import UserCreate, UserRead

from app.services import user


router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "login": current_user.login}



@router.get(
    "",
    response_model=List[UserRead],
    summary="get all users"
)
async def get_all_user(session: AsyncSession = Depends(get_async_session)):
    return await user.get_all_users(session)