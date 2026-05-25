from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session

from app.models.schemas.system_schemas import (
    SystemSchemasCreate,
    SystemSchemasPreview,
    SystemSchemasRead,
)

from app.dependencies.auth import MasterUser

from app.services.system_schemas import (
    create_system_schema,
    delete_system_schema,
    get_all_system_schemas,
    get_system_schema_by_id,
    get_system_schema_by_name,
    update_system_schema,
)

router = APIRouter(
    prefix="/systems-schemas",
    tags=["Systems Schemas"],
)


@router.post(
    "",
    response_model=SystemSchemasRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_schema_api(
    schemadata: SystemSchemasCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await create_system_schema(
            schema_data=schemadata,
            session=session,
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.get(
    "",
    response_model=List[SystemSchemasPreview],
)
async def get_all_schemas_api(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_system_schemas(session)


@router.get(
    "/{schema_id}",
    response_model=SystemSchemasRead,
)
async def get_schema_by_id(
    schema_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    schema = await get_system_schema_by_id(
        session=session,
        schema_id=schema_id,
    )

    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System schema not found",
        )

    return schema


@router.get(
    "/by_name/{schema_name}",
    response_model=SystemSchemasRead,
)
async def get_schema_by_name(
    schema_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    schema = await get_system_schema_by_name(
        session=session,
        schema_name=schema_name,
    )

    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System schema not found",
        )

    return schema


@router.put(
    "/{schema_id}",
    response_model=SystemSchemasRead,
)
async def update_schema_api(
    schema_id: int,
    schema_data: SystemSchemasCreate,
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        updated_schema = await update_system_schema(
            schema_id=schema_id,
            schema_data=schema_data,
            session=session,
        )

        if not updated_schema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System schema not found",
            )

        return updated_schema

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )


@router.delete(
    "/{schema_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_schema_api(
    schema_id: int,
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        deleted = await delete_system_schema(
            schema_id=schema_id,
            session=session,
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Foreign key violation: {e}",
        )
