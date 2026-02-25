from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.quest_schemas import QuestCreate, QuestUpdate

#from app.models.orm.models import Quest
#
#async def create_quest(session: AsyncSession, broker: Broker, quest_data: QuestCreate):
#    new_quest_orm = Quest(**quest_data.model_dump())
#
#    session.add(new_quest_orm)
#
#    await session.commit()
#    await session.refresh(new_quest_orm)
#
#    await broker.publish_quest(f"newF-quest", new_quest_orm)
#
#    return new_quest_orm
#
#
#async def get_all_quests(session: AsyncSession):
#    result = await session.execute(select(Quest))
#
#    return result.scalars().all()
#
#
#async def get_quest_by_id(session: AsyncSession, quest_id: int):
#    result = await session.get(Quest, quest_id)
#
#    return result
#
#
#async def update_quest(
#        session: AsyncSession,
#        broker: Broker,
#        quest_id: int,
#        update_data: QuestUpdate
#):
#    quest_orm = await get_quest_by_id(session, quest_id)
#
#    if quest_orm is None:
#        return None
#
#    update_fields = update_data.model_dump(exclude_unset=True)
#
#    if not update_fields:
#        return quest_orm
#
#    for key, value in update_fields.items():
#        setattr(quest_orm, key, value)
#
#    await session.commit()
#    await session.refresh(quest_orm)
#
#    await broker.publish_quest(f"updated-quest", quest_orm)
#
#    return quest_orm
#
#
#async def delete_quest(session: AsyncSession, quest_id: int):
#    result = await get_quest_by_id(session, quest_id)
#    await session.delete(result)
#    await session.commit()
#
#    return
#