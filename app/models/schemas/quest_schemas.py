from pydantic import BaseModel
from typing import Optional


class QuestCreate(BaseModel):
    title: str
    short_description: str
    description: str
    is_locked: Optional[bool] = False


class QuestUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    is_locked: Optional[bool] = None


class QuestRead(BaseModel):
    id: int
    title: str
    short_description: str
    description: str
    is_locked: bool

    class Config:
        from_attributes = True
