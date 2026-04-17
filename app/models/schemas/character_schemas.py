from typing import Any, Dict

from pydantic import BaseModel, Json


class CharacterRead(BaseModel):
    id: int
    user_id: int

    name: str
    description: str
    data_fields: Dict[str, Any] 

    class Config:
        from_attributes = True


class CharacterRequest(BaseModel):
    name: str
    description: str
    data_fields: Dict[str, Any] 

    class Config:
        from_attributes = True

class CharacterCreate(CharacterRequest):
    user_id: int