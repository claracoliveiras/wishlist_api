from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class CollectionBase(BaseModel):
    name: str | None = None
    owner_id: uuid.UUID | None = None
    collection_img: str | None = None


class CollectionCreate(CollectionBase):
    name: str
    owner_id: uuid.UUID
    collection_img: str


class CollectionUpdate(CollectionBase):
    pass


class CollectionRead(CollectionBase):
    id: uuid.UUID
    name: str
    owner_id: uuid.UUID
    collection_img: str

    model_config = ConfigDict(from_attributes=True)
