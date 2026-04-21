from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    contact_info: Optional[str] = None
    role: Optional[str] = "player"


class UserRead(BaseModel):
    id: int
    login: str
    contact_info: Optional[str]
    role: str

    class Config:
        from_attributes = True

class UserSetRole(BaseModel):
    id: int
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
