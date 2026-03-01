from typing import TypeVar, Type, Generic, List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.db import Base, get_async_session

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model_class: Type[ModelType]):
        self.session = session
        self.model_class = model_class

    async def create(self, **kwargs) -> ModelType:
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[ModelType]:
        result = await self.session.execute(
            select(self.model_class)
        )
        return result.scalars().all()

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        await self.session.execute(
            update(self.model_class).where(self.model_class.id == id).values(**kwargs)
        )
        await self.session.commit()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model_class).where(self.model_class.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0