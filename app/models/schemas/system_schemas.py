from typing import Any, Dict

from pydantic import BaseModel


class SystemSchemasPreview(BaseModel):
    name: str

    class Config:
        from_attributes = True


class SystemSchemasRead(BaseModel):
    id: int

    name: str
    schema: str

    class Config:
        from_attributes = True


class SystemSchemasCreate(BaseModel):
    name: str
    schema: str

    class Config:
        from_attributes = True
