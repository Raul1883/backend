from typing import Any, Dict

from pydantic import BaseModel


class ApplicationRead(BaseModel):
    id: int

    user_id: int
    session_id: int
    character_id: int

    comment: str
    status: str

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    user_id: int
    session_id: int
    character_id: int

    comment: str
    status: str

    class Config:
        from_attributes = True


class ApplicationRequest(BaseModel):
    session_id: int
    character_id: int

    comment: str

    class Config:
        from_attributes = True


class ApplicationsCount(BaseModel):
    count: int

    class Config:
        from_attributes = True
