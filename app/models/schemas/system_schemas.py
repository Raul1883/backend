from typing import Any, Dict

from pydantic import BaseModel


class SystemSchemasPreview(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SystemSchemasRead(BaseModel):
    id: int

    name: str
    schema: Any

    class Config:
        from_attributes = True


class SystemSchemasCreate(BaseModel):
    name: str
    schema: Any

    class Config:
        from_attributes = True
