from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    owner_id: uuid.UUID | None = None
    item_url: str | None = None
    item_img: str | None = None


class ItemCreate(ItemBase):
    owner_id: uuid.UUID
    item_url: str
    item_img: str


class ItemUpdate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    item_url: str
    item_img: str

    model_config = ConfigDict(from_attributes=True)
