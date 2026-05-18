from typing import Dict, Optional, List, Any

from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import Base
from app.exceptions.service_exceptions import (
    ForeignKeyViolationError,
    AttributeAlreadyExistsError,
    AttributeNotFound,
    PermissionDeniedError,
)
from app.models.schemas.character_schemas import (
    CharacterRead,
    CharacterRequest,
    CharacterCreate,
)
from app.models.orm.models import Character, User
from sqlalchemy.orm import selectinload

from app.db.repositories import BaseRepository

from app.exceptions.service_exceptions import ActionNotAllowedError

## Characters


async def create_character(
    session: AsyncSession, user: User, character_data: CharacterRequest
):

    try:
        character_repository = BaseRepository(session, Character)
        new_orm = await character_repository.create(
            **character_data.model_dump(), user_id=user.id
        )
        return await get_character_by_id(session, new_orm.id, user)
    except IntegrityError as e:
        raise ForeignKeyViolationError(f"Foreign key violation: {e}")


## Master only
async def get_all_characters(session: AsyncSession):
    result = await session.execute(
        select(Character).options(
            selectinload(Character.owner),
        )
    )

    return result.scalars().all()


async def get_all_my_characters(session: AsyncSession, user: User):
    result = await session.execute(
        select(Character)
        .where(Character.user_id == user.id)
        .options(
            selectinload(Character.owner),
        )
    )

    return result.scalars().all()


async def get_character_by_id(session: AsyncSession, character_id: int, user: User):

    await check_permission_to_edit(session, character_id, user)

    result = await session.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(
            selectinload(Character.owner),
        )
    )
    orm = result.scalars().one_or_none()

    return orm


async def update_character(
    session: AsyncSession,
    character_id: int,
    user: User,
    character_data: CharacterRequest,
):

    await check_permission_to_edit(session, character_id, user)

    repository = BaseRepository(session, Character)

    await repository.update(
        character_id, **character_data.model_dump(exclude_unset=True), user_id=user.id
    )
    return await get_character_by_id(session, character_id, user)


async def delete_character(session: AsyncSession, character_id: int, user: User):
    await check_permission_to_edit(session, character_id, user)
    repository = BaseRepository(session, Character)
    return await repository.delete(character_id)


## Characters attributes


def get_character_repository(session: AsyncSession) -> BaseRepository:
    return BaseRepository(session, Character)


async def check_permission_to_edit(
    session: AsyncSession, character_id: int, user: User
):
    result = await session.execute(
        select(Character)
        .where(Character.id == character_id)
        .options(
            selectinload(Character.owner),
        )
    )

    character_old = result.scalars().one_or_none()
    if character_old.user_id != user.id and user.role != "master":
        raise PermissionDeniedError
