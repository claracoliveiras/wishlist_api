from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None
    profile_picture: str | None = None
    banner_picture: str | None = None


class UserCreate(UserBase):
    id: str
    username: str
    email: str


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
