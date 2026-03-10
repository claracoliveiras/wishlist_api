from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.models.following import Following
from app.schemas.following import FollowingCreate, FollowingRead, FollowingUpdate
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError
from app.services.following_service import (
    create_following,
    delete_following,
    get_following,
    list_followings,
    update_following,
)

router = APIRouter(prefix="/following", tags=["following"])


@router.post("", response_model=FollowingRead, status_code=status.HTTP_201_CREATED)
def create_following_route(
    payload: FollowingCreate,
    db: Session = Depends(get_db),
) -> FollowingRead:
    following = Following(**payload.model_dump())
    try:
        return create_following(db, following)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[FollowingRead])
def list_following_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    follower_id: uuid.UUID | None = Query(default=None),
    followee_id: uuid.UUID | None = Query(default=None),
) -> list[FollowingRead]:
    try:
        return list_followings(
            db,
            skip=skip,
            limit=limit,
            follower_id=follower_id,
            followee_id=followee_id,
        )
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{following_id}", response_model=FollowingRead)
def get_following_route(following_id: uuid.UUID, db: Session = Depends(get_db)) -> FollowingRead:
    try:
        following = get_following(db, following_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if following is None:
        raise HTTPException(status_code=404, detail="Following record not found")
    return following


@router.patch("/{following_id}", response_model=FollowingRead)
def update_following_route(
    following_id: uuid.UUID,
    payload: FollowingUpdate,
    db: Session = Depends(get_db),
) -> FollowingRead:
    try:
        following = get_following(db, following_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if following is None:
        raise HTTPException(status_code=404, detail="Following record not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(following, key, value)

    try:
        return update_following(db, following)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/{following_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_following_route(following_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    try:
        following = get_following(db, following_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if following is None:
        raise HTTPException(status_code=404, detail="Following record not found")

    try:
        delete_following(db, following)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
