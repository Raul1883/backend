from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.session_schemas import SessionCreate, SessionRead
from app.models.orm.models import Session
from sqlalchemy.orm import selectinload


async def create_session(session: AsyncSession, session_data: SessionCreate):
    new_session_orm = Session(**session_data.model_dump())

    session.add(new_session_orm)

    await session.commit()
    await session.refresh(new_session_orm)

    return new_session_orm



async def get_all_sessions(session: AsyncSession):
    print(Session)
    print(type(Session))
    print(Session.master)
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
    result = await session.get(Session, session_id)

    return result
