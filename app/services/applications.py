from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.service_exceptions import (
    IncorrectStatusError,
    PermissionDeniedError,
)
from app.models.orm.models import Application, User
from app.models.schemas.application_schemas import ApplicationRequest


async def create_application(
    session: AsyncSession, application_data: ApplicationRequest, user: User
):
    new_application = Application(
        user_id=user.id,
        session_id=application_data.session_id,
        character_id=application_data.character_id,
        comment=application_data.comment,
        status="pending",
    )
    session.add(new_application)
    await session.commit()
    await session.refresh(new_application)
    return new_application


async def revoke_application(session: AsyncSession, application_id: int, user: User):
    application = await session.get(Application, application_id)

    if user.role != "master" and user.id != application.user_id:
        raise PermissionDeniedError

    if application:
        application.status = "rejected"
        await session.commit()
        await session.refresh(application)
        return application
    return None


async def get_all_applications(session: AsyncSession):
    result = await session.execute(select(Application))
    return result.scalars().all()


async def get_application_by_id(session: AsyncSession, application_id: int):
    return await session.get(Application, application_id)


async def get_application_by_session_id(session: AsyncSession, session_id: int):
    result = await session.execute(
        select(Application).where(Application.session_id == session_id)
    )
    return result.scalars()


async def get_application_count_by_session_id(session: AsyncSession, session_id: int):
    from sqlalchemy import func, select

    result = await session.execute(
        select(func.count())
        .select_from(Application)
        .where(Application.session_id == session_id)
    )
    return result.scalar()


async def set_application_status(
    session: AsyncSession, application_id: int, status: str
):
    if status not in ["pending", "approved", "rejected"]:
        raise IncorrectStatusError

    application = await session.get(Application, application_id)
    if application:
        application.status = status
        await session.commit()
        await session.refresh(application)
        return application
    return None


async def delete_application_by_id(session: AsyncSession, application_id: int, user: User):
    application = await session.get(Application, application_id)

    if user.role != "master" and user.id != application.user_id:
        raise PermissionDeniedError
    
    await session.delete(application)
    await session.commit()

    return None
