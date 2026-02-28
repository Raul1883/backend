from pydantic import BaseModel


class NamedEntity(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
