from app.db.repositories import BaseRepository
from app.exceptions.service_exceptions import SchemaAlreadyExistsError
from app.exceptions.service_exceptions import SchemaAlreadyExistsError
from app.models.orm.models import SystemSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


from app.models.schemas.system_schemas import SystemSchemasCreate


async def get_all_system_schemas(session: AsyncSession):
    repository = BaseRepository(session, SystemSchema)
    return await repository.get_all()


async def create_system_schema(session: AsyncSession, schema_data: SystemSchemasCreate):
    if await get_system_schema_by_name(session, schema_data.name):
        raise SchemaAlreadyExistsError(name=schema_data.name)

    repository = BaseRepository(session, SystemSchema)
    return await repository.create(**schema_data.model_dump())


async def get_system_schema_by_name(session: AsyncSession, name: str):
    result = await session.execute(
        select(SystemSchema).where(SystemSchema.name == name)
    )
    return result.scalar_one_or_none()


async def update_system_schema(session: AsyncSession, schema_data: SystemSchemasCreate):
    result = await get_system_schema_by_name(session, schema_data.name)
    if not result:
        return None

    repository = BaseRepository(session, SystemSchema)
    return await repository.update(result.id, **schema_data.model_dump())


async def delete_system_schema(session: AsyncSession, name: str):
    result = await get_system_schema_by_name(session, name)
    if not result:
        return None

    repository = BaseRepository(session, SystemSchema)
    await repository.delete(result.id)
