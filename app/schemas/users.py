from __future__ import annotations
import uuid

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None
    profile_picture: str | None = None
    banner_picture: str | None = None


class UserCreate(UserBase):
    id: uuid.UUID
    username: str
    email: str
    password: str = Field(min_length=8)


class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8)


class UserRead(UserBase):
    id: uuid.UUID
    username: str
    email: str
    profile_picture: str
    banner_picture: str

    model_config = ConfigDict(from_attributes=True)
