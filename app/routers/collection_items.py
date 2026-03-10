from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.models.collection_items import CollectionItems
from app.schemas.collection_items import (
    CollectionItemCreate,
    CollectionItemRead,
    CollectionItemUpdate,
)
from app.services.collection_items_service import (
    create_collection_item,
    delete_collection_item,
    get_collection_item,
    list_collection_items,
    update_collection_item,
)
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError

router = APIRouter(prefix="/collection-items", tags=["collection_items"])


@router.post("", response_model=CollectionItemRead, status_code=status.HTTP_201_CREATED)
def create_collection_item_route(
    payload: CollectionItemCreate,
    db: Session = Depends(get_db),
) -> CollectionItemRead:
    collection_item = CollectionItems(**payload.model_dump())
    try:
        return create_collection_item(db, collection_item)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[CollectionItemRead])
def list_collection_items_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    collection_id: uuid.UUID | None = Query(default=None),
    item_id: uuid.UUID | None = Query(default=None),
) -> list[CollectionItemRead]:
    try:
        return list_collection_items(
            db,
            skip=skip,
            limit=limit,
            collection_id=collection_id,
            item_id=item_id,
        )
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{collection_item_id}", response_model=CollectionItemRead)
def get_collection_item_route(
    collection_item_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> CollectionItemRead:
    try:
        collection_item = get_collection_item(db, collection_item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection_item is None:
        raise HTTPException(status_code=404, detail="Collection item not found")
    return collection_item


@router.patch("/{collection_item_id}", response_model=CollectionItemRead)
def update_collection_item_route(
    collection_item_id: uuid.UUID,
    payload: CollectionItemUpdate,
    db: Session = Depends(get_db),
) -> CollectionItemRead:
    try:
        collection_item = get_collection_item(db, collection_item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection_item is None:
        raise HTTPException(status_code=404, detail="Collection item not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(collection_item, key, value)

    try:
        return update_collection_item(db, collection_item)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/{collection_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection_item_route(
    collection_item_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> None:
    try:
        collection_item = get_collection_item(db, collection_item_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection_item is None:
        raise HTTPException(status_code=404, detail="Collection item not found")

    try:
        delete_collection_item(db, collection_item)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
