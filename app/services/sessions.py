from typing import Dict

from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import Base
from app.exceptions.service_exceptions import (
    ForeignKeyViolationError,
    AttributeAlreadyExistsError,
    AttributeNotFound,
)
from app.models.schemas.named_entity import NamedEntity
from app.models.schemas.session_schemas import (
    CreateGenreSchema,
    SessionCreate,
    SessionRead,
)
from app.models.orm.models import Company, Genre, Session, System, User
from sqlalchemy.orm import selectinload

from app.db.repositories import BaseRepository

from app.exceptions.service_exceptions import ActionNotAllowedError

## Sessions


async def create_session(session: AsyncSession, session_data: SessionCreate):

    user_repository = BaseRepository(session, User)
    creator = await user_repository.get_by_id(session_data.master_id)

    if creator.role != "master":
        raise ActionNotAllowedError(creator.role)

    try:
        session_repository = BaseRepository(session, Session)
        new_orm = await session_repository.create(**session_data.model_dump())
        return await get_session_by_id(session, new_orm.id)
    except IntegrityError as e:
        raise ForeignKeyViolationError(f"Foreign key violation: {e}")


async def get_all_sessions(session: AsyncSession):
    result = await session.execute(
        select(Session).options(
            selectinload(Session.master),
            selectinload(Session.system),
            selectinload(Session.genre),
            selectinload(Session.company),
        )
    )

    return result.scalars().all()


async def get_session_by_id(session: AsyncSession, session_id: int):

    result = await session.execute(
        select(Session)
        .where(Session.id == session_id)
        .options(
            selectinload(Session.master),
            selectinload(Session.system),
            selectinload(Session.genre),
            selectinload(Session.company),
        )
    )
    orm = result.scalars().one_or_none()

    return await validate_session_orm(orm)


async def validate_session_orm(orm: Session | None):
    if orm is None:
        return None

    if orm.company_id is None:
        orm.company_id = -1
        orm.company = Company(id = -1, title="OneShot", description="desc")

    return orm

async def update_session(
    session: AsyncSession, session_id: int, session_data: SessionCreate
):
    repository = BaseRepository(session, Session)
    await repository.update(session_id, **session_data.model_dump(exclude_unset=True))
    return await get_session_by_id(session, session_id)


async def delete_session(session: AsyncSession, session_id: int):
    repository = BaseRepository(session, Session)
    return await repository.delete(session_id)


## Sessions attributes


def get_atribute_repository(session: AsyncSession, model_class: Base) -> BaseRepository:
    return BaseRepository(session, model_class)


async def create_attribute(
    session: AsyncSession, model_class: Base, data: CreateGenreSchema
):
    try:
        data = data.model_dump()
        repository = get_atribute_repository(session, model_class)
        return await repository.create(**data)
    except IntegrityError:
        raise AttributeAlreadyExistsError(data)


async def get_all_attributes(session: AsyncSession, model_class: Base):
    repository = get_atribute_repository(session, model_class)
    return await repository.get_all()


async def get_attribute_by_id(session: AsyncSession, model_class: Base, id: int):
    repository = get_atribute_repository(session, model_class)
    result = await repository.get_by_id(id)
    if result is None:
        raise AttributeNotFound(id)
    return result


async def delete_attribute(session: AsyncSession, model_class: Base, id: int):
    repository = get_atribute_repository(session, model_class)
    await repository.delete(id)
