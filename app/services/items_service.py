from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.items import Items
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError


def create_item(db: Session, item: Items) -> Items:
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to create item due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to create item") from exc


def get_item(db: Session, item_id: uuid.UUID) -> Items | None:
    try:
        return db.scalar(select(Items).where(Items.id == item_id))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch item") from exc


def list_items(
    db: Session, skip: int = 0, limit: int = 100, owner_id: str | None = None
) -> list[Items]:
    try:
        query = select(Items)
        if owner_id:
            query = query.where(Items.owner_id == owner_id)
        return list(db.scalars(query.offset(skip).limit(limit)).all())
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to list items") from exc


def update_item(db: Session, item: Items) -> Items:
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to update item due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to update item") from exc


def delete_item(db: Session, item: Items) -> None:
    try:
        db.delete(item)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to delete item") from exc
