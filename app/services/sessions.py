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
from app.models.schemas.session_schemas import SessionCreate, SessionRead
from app.models.orm.models import Genre, Session, System, User
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

        return new_orm
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
    repository = BaseRepository(session, Genre)
    return await repository.get_by_id(session_id)


## Sessions attributes


def get_atribute_repository(session: AsyncSession, model_class: Base) -> BaseRepository:
    return BaseRepository(session, model_class)


async def create_attribute(
    session: AsyncSession, model_class: Base, data: Dict[str, str]
):
    try:
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
