from pydantic import BaseModel
from typing import Optional


class SessionCreate(BaseModel):
    title: str
    description: Optional[str]
    scheduled_at: Optional[str] = None
    master_id: int
    system_id: int
    genre_id: int
    company: Optional[str] = None


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None


class SessionRead(BaseModel):
    id: int
    title: str
    short_description: str
    description: str
    is_locked: bool

    class Config:
        from_attributes = True
