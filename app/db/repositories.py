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
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(id)
        
        stmt = (
            update(self.model_class)
            .where(self.model_class.id == id)
            .values(**update_data)
            .returning(self.model_class)  
        )
        
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        updated_obj = result.scalar_one_or_none()
        
        if updated_obj:
            await self.session.refresh(updated_obj)
            
        return updated_obj

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model_class).where(self.model_class.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0