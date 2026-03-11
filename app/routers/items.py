from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.models.items import Items
from app.schemas.items import ItemCreate, ItemRead, ItemUpdate
from app.services.auth_service import get_current_user
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError
from app.services.items_service import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_route(payload: ItemCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)) -> ItemRead:
    data = payload.model_dump()
    data["owner_id"] = current_user.id
    item = Items(**data)
    try:
        return create_item(db, item)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[ItemRead])
def list_items_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    owner_id: str | None = Query(default=None),
) -> list[ItemRead]:
    try:
        return list_items(db, skip=skip, limit=limit, owner_id=owner_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{item_id}", response_model=ItemRead)
def get_item_route(item_id: uuid.UUID, db: Session = Depends(get_db)) -> ItemRead:
    try:
        item = get_item(db, item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ItemRead)
def update_item_route(
    item_id: uuid.UUID,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
) -> ItemRead:
    try:
        item = get_item(db, item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    try:
        return update_item(db, item)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_route(item_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    try:
        item = get_item(db, item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        delete_item(db, item)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
