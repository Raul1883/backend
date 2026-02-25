from pydantic import BaseModel


class NamedEntity(BaseModel):
    id: int
    name: str