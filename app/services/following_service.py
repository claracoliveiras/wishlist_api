from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.following import Following
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError


def create_following(db: Session, following: Following) -> Following:
    try:
        db.add(following)
        db.commit()
        db.refresh(following)
        return following
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to create following due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to create following") from exc


def get_following(db: Session, following_id: uuid.UUID) -> Following | None:
    try:
        return db.scalar(select(Following).where(Following.id == following_id))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch following") from exc


def list_followings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    follower_id: uuid.UUID | None = None,
    followee_id: uuid.UUID | None = None,
) -> list[Following]:
    try:
        query = select(Following)
        if follower_id is not None:
            query = query.where(Following.follower_id == follower_id)
        if followee_id is not None:
            query = query.where(Following.followee_id == followee_id)
        return list(db.scalars(query.offset(skip).limit(limit)).all())
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to list followings") from exc


def update_following(db: Session, following: Following) -> Following:
    try:
        db.add(following)
        db.commit()
        db.refresh(following)
        return following
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to update following due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to update following") from exc


def delete_following(db: Session, following: Following) -> None:
    try:
        db.delete(following)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to delete following") from exc
