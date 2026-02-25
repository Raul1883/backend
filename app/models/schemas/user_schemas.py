from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    contact_info: Optional[str] = None
    roles: Optional[str] = "player"


class UserRead(BaseModel):
    id: int
    login: str
    contact_info: Optional[str]
    roles: str
