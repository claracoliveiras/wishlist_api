from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class CollectionItemBase(BaseModel):
    item_id: uuid.UUID | None = None
    collection_id: uuid.UUID | None = None


class CollectionItemCreate(CollectionItemBase):
    id: uuid.UUID
    item_id: uuid.UUID
    collection_id: uuid.UUID


class CollectionItemUpdate(CollectionItemBase):
    pass


class CollectionItemRead(CollectionItemBase):
    id: uuid.UUID
    item_id: uuid.UUID
    collection_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
