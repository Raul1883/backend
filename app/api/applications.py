from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.db import get_async_session
from app.dependencies.auth import MasterUser, get_current_user
from app.models.orm.models import User
from app.models.schemas.application_schemas import ApplicationsCount, ApplicationRead, ApplicationRequest
from app.services.applications import (
    create_application,
    delete_application_by_id,
    get_all_applications,
    get_application_by_id,
    get_application_by_session_id,
    get_application_count_by_session_id,
    revoke_application,
    set_application_status,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post("", response_model=ApplicationRead)
async def create(
    application_data: ApplicationRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_application(
        session=session, application_data=application_data, user=user
    )


@router.get("/{application_id}", response_model=ApplicationRead)
async def get_by_id(
    application_id: int,
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    application = await get_application_by_id(
        session=session, application_id=application_id
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("", response_model=list[ApplicationRead])
async def get_all(
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_applications(session)


@router.get("/by_sessions/data/{session_id}", response_model=list[ApplicationRead])
async def get_count_by_session(
    session_id: int,
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_application_by_session_id(session,session_id)


@router.get("/by_sessions/count/{session_id}", response_model=ApplicationsCount)
async def get_count_by_session(
    session_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_application_count_by_session_id(session,session_id)
    return ApplicationsCount(count=result)


@router.put("/{application_id}/status", response_model=ApplicationRead)
async def set_status(
    application_id: int,
    status: str,
    user: MasterUser,
    session: AsyncSession = Depends(get_async_session),
):
    application = await set_application_status(session, application_id, status)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/revoke/{application_id}", response_model=ApplicationRead)
async def revoke(
    application_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    application = await revoke_application(session, application_id, user)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application



@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    application_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    application = await delete_application_by_id(session, application_id, user)

    return application