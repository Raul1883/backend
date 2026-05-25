import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import SchemaAlreadyExistsError
from app.models.orm.models import SystemSchema
from app.models.schemas.system_schemas import SystemSchemasCreate


async def get_all_system_schemas(session: AsyncSession):
    repository = BaseRepository(session, SystemSchema)
    return await repository.get_all()


async def create_system_schema(
    session: AsyncSession,
    schema_data: SystemSchemasCreate,
):
    schema_data_dict = schema_data.model_dump()
    schema_data_dict["schema"] = json.dumps(schema_data_dict["schema"])

    repository = BaseRepository(session, SystemSchema)

    return await repository.create(**schema_data_dict)


async def get_system_schema_by_id(
    session: AsyncSession,
    schema_id: int,
):
    result = await session.execute(
        select(SystemSchema).where(SystemSchema.id == schema_id)
    )

    res = result.scalar_one_or_none()

    if res:
        res.schema = json.loads(res.schema)

    return res


async def get_system_schema_by_name(
    session: AsyncSession,
    schema_name: str,
):
    result = await session.execute(
        select(SystemSchema).where(SystemSchema.name == schema_name)
    )

    res = result.scalar_one_or_none()

    if res:
        res.schema = json.loads(res.schema)

    return res


async def update_system_schema(
    session: AsyncSession,
    schema_id: int,
    schema_data: SystemSchemasCreate,
):
    result = await session.execute(
        select(SystemSchema).where(SystemSchema.id == schema_id)
    )

    res = result.scalar_one_or_none()

    if not res:
        return None

    schema_data_dict = schema_data.model_dump()
    schema_data_dict["schema"] = json.dumps(schema_data_dict["schema"])

    repository = BaseRepository(session, SystemSchema)

    return await repository.update(
        schema_id,
        **schema_data_dict,
    )


async def delete_system_schema(
    session: AsyncSession,
    schema_id: int,
):
    result = await session.execute(
        select(SystemSchema).where(SystemSchema.id == schema_id)
    )

    res = result.scalar_one_or_none()

    if not res:
        return None

    repository = BaseRepository(session, SystemSchema)

    await repository.delete(schema_id)
