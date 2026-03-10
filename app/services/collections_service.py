from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.collections import Collections
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError


def create_collection(db: Session, collection: Collections) -> Collections:
    try:
        db.add(collection)
        db.commit()
        db.refresh(collection)
        return collection
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to create collection due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to create collection") from exc


def get_collection(db: Session, collection_id: uuid.UUID) -> Collections | None:
    try:
        return db.scalar(select(Collections).where(Collections.id == collection_id))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch collection") from exc


def list_collections(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: uuid.UUID | None = None,
) -> list[Collections]:
    try:
        query = select(Collections)
        if owner_id is not None:
            query = query.where(Collections.owner_id == owner_id)
        return list(db.scalars(query.offset(skip).limit(limit)).all())
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to list collections") from exc


def update_collection(db: Session, collection: Collections) -> Collections:
    try:
        db.add(collection)
        db.commit()
        db.refresh(collection)
        return collection
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to update collection due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to update collection") from exc


def delete_collection(db: Session, collection: Collections) -> None:
    try:
        db.delete(collection)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to delete collection") from exc
