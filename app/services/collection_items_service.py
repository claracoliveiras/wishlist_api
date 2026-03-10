from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.collection_items import CollectionItems
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError


def create_collection_item(db: Session, collection_item: CollectionItems) -> CollectionItems:
    try:
        db.add(collection_item)
        db.commit()
        db.refresh(collection_item)
        return collection_item
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError(
            "Failed to create collection item due to a constraint conflict"
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to create collection item") from exc


def get_collection_item(db: Session, collection_item_id: uuid.UUID) -> CollectionItems | None:
    try:
        return db.scalar(select(CollectionItems).where(CollectionItems.id == collection_item_id))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch collection item") from exc


def list_collection_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    collection_id: uuid.UUID | None = None,
    item_id: uuid.UUID | None = None,
) -> list[CollectionItems]:
    try:
        query = select(CollectionItems)
        if collection_id is not None:
            query = query.where(CollectionItems.collection_id == collection_id)
        if item_id is not None:
            query = query.where(CollectionItems.item_id == item_id)
        return list(db.scalars(query.offset(skip).limit(limit)).all())
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to list collection items") from exc


def update_collection_item(db: Session, collection_item: CollectionItems) -> CollectionItems:
    try:
        db.add(collection_item)
        db.commit()
        db.refresh(collection_item)
        return collection_item
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError(
            "Failed to update collection item due to a constraint conflict"
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to update collection item") from exc


def delete_collection_item(db: Session, collection_item: CollectionItems) -> None:
    try:
        db.delete(collection_item)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to delete collection item") from exc
