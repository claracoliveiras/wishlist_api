from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class FollowingBase(BaseModel):
    followee_id: uuid.UUID | None = None
    follower_id: uuid.UUID | None = None


class FollowingCreate(FollowingBase):
    id: uuid.UUID
    followee_id: uuid.UUID
    follower_id: uuid.UUID


class FollowingUpdate(FollowingBase):
    pass


class FollowingRead(FollowingBase):
    id: uuid.UUID
    followee_id: uuid.UUID
    follower_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
