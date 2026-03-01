from pydantic import BaseModel
from typing import Optional

from app.models.schemas.named_entity import NamedEntity


class SessionCreate(BaseModel):
    title: str
    description: Optional[str]
    scheduled_at: Optional[str] = None
    master_id: int
    system_id: int
    genre_id: int
    company_id: Optional[int] = None


class SessionRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    scheduled_at: Optional[str] = None
    master: NamedEntity
    system: NamedEntity
    genre: NamedEntity
    company: NamedEntity

    class Config:
        from_attributes = True

class GenreSchema(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True

class SystemSchema(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True

class CompanySchema(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True
