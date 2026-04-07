from pydantic import BaseModel
from typing import Optional

from app.models.schemas.named_entity import NamedEntity
from app.models.schemas.user_schemas import UserRead


class GenreSchema(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


class CreateGenreSchema(BaseModel):
    text: str

    class Config:
        from_attributes = True


class SystemSchema(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


class CreateSystemSchema(BaseModel):
    text: str

    class Config:
        from_attributes = True


class CompanySchema(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True

class CreateCompanySchema(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True


class ShortCompanySchema(BaseModel):
    id: Optional[int]
    text: str

    class Config:
        from_attributes = True


class SessionRequest(BaseModel):
    title: str
    description: Optional[str]
    scheduled_at: Optional[str] = None
    system_id: int
    genre_id: int
    company_id: Optional[int] = None


class SessionCreate(SessionRequest):
    master_id: int

class SessionRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    scheduled_at: Optional[str] = None
    master: UserRead
    system: SystemSchema
    genre: GenreSchema
    company: Optional[CompanySchema] = None

    class Config:
        from_attributes = True


class SessionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    scheduled_at: str | None = None
    master_id: int | None = None
    system_id: int | None = None
    genre_id: int | None = None
    company_id: int | None = None

    class Config:
        from_attributes = True
