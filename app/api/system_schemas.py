from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.db import get_async_session
from app.models.orm.models import Character, User
from app.models.schemas.character_schemas import (
    CharacterRead,
    CharacterCreate,
    CharacterRequest,
)
from app.models.schemas.system_schemas import (
    SystemSchemasCreate,
    SystemSchemasPreview,
    SystemSchemasRead,
)
from app.services.characters import (
    create_character,
    get_all_characters,
    get_all_my_characters,
    get_character_by_id,
    update_character,
    delete_character,
)
from app.dependencies.auth import AnyUser, MasterUser, get_current_user
from app.services.system_schemas import (
    create_system_schema,
    delete_system_schema,
    get_all_system_schemas,
    get_system_schema_by_name,
    update_system_schema,
)

router = APIRouter(
    prefix="/systems-schemas",
    tags=["Systems Schemas"],
)


@router.post("", response_model=SystemSchemasRead, status_code=status.HTTP_201_CREATED)
async def create_schema_api(
    schemadata: SystemSchemasCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await create_system_schema(schema_data=schemadata, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.get("", response_model=List[SystemSchemasPreview])
async def get_all_schemas_api(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_system_schemas(session)


@router.get("/{name}", response_model=SystemSchemasRead)
async def get_schema_by_name(
    name: str,
    session: AsyncSession = Depends(get_async_session),
):
    schema = await get_system_schema_by_name(session=session, name=name)
    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System schema not found",
        )
    return schema


@router.put("", response_model=SystemSchemasRead)
async def update_schema_api(
    schema_data: SystemSchemasCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await update_system_schema(schema_data=schema_data, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schema_api(
    name: str,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        await delete_system_schema(name=name, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )
