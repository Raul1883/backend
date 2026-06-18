from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.dependencies.auth import AnyUser, MasterUser, get_current_user
from app.models.orm.models import User
from app.models.schemas.user_schemas import UserCreate, UserRead, UserSetRole

from app.services import user


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/profile", response_model=UserRead)
async def get_me(current_user: AnyUser):
    return {
        "id": current_user.id,
        "login": current_user.login,
        "role": current_user.role,
        "contact_info": current_user.contact_info,
    }


@router.get("", response_model=List[UserRead], summary="get all users")
async def get_all_user(current_user: MasterUser, session: AsyncSession = Depends(get_async_session)):
    return await user.get_all_users(session)


@router.patch("/user", response_model=UserRead)
async def set_role(data: UserSetRole, current_user: MasterUser, session: AsyncSession = Depends(get_async_session)):
    return await user.set_user_role(session, data)


