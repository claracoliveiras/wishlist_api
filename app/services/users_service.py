from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.users import Users
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError


def create_user(db: Session, user: Users) -> Users:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to create user due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to create user") from exc


def get_user(db: Session, user_id: str) -> Users | None:
    try:
        return db.scalar(select(Users).where(Users.id == user_id))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch user") from exc


def get_user_by_username(db: Session, username: str) -> Users | None:
    try:
        return db.scalar(select(Users).where(Users.username == username))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch user by username") from exc


def get_user_by_email(db: Session, email: str) -> Users | None:
    try:
        return db.scalar(select(Users).where(Users.email == email))
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to fetch user by email") from exc


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[Users]:
    try:
        return list(db.scalars(select(Users).offset(skip).limit(limit)).all())
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to list users") from exc


def update_user(db: Session, user: Users) -> Users:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise ServiceConflictError("Failed to update user due to a constraint conflict") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to update user") from exc


def delete_user(db: Session, user: Users) -> None:
    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to delete user") from exc
