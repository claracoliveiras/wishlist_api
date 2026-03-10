from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.models.collections import Collections
from app.schemas.collections import CollectionCreate, CollectionRead, CollectionUpdate
from app.services.collections_service import (
    create_collection,
    delete_collection,
    get_collection,
    list_collections,
    update_collection,
)
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("", response_model=CollectionRead, status_code=status.HTTP_201_CREATED)
def create_collection_route(
    payload: CollectionCreate,
    db: Session = Depends(get_db),
) -> CollectionRead:
    collection = Collections(**payload.model_dump())
    try:
        return create_collection(db, collection)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[CollectionRead])
def list_collections_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    owner_id: uuid.UUID | None = Query(default=None),
) -> list[CollectionRead]:
    try:
        return list_collections(db, skip=skip, limit=limit, owner_id=owner_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{collection_id}", response_model=CollectionRead)
def get_collection_route(
    collection_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> CollectionRead:
    try:
        collection = get_collection(db, collection_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.patch("/{collection_id}", response_model=CollectionRead)
def update_collection_route(
    collection_id: uuid.UUID,
    payload: CollectionUpdate,
    db: Session = Depends(get_db),
) -> CollectionRead:
    try:
        collection = get_collection(db, collection_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(collection, key, value)

    try:
        return update_collection(db, collection)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection_route(collection_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    try:
        collection = get_collection(db, collection_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")

    try:
        delete_collection(db, collection)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
