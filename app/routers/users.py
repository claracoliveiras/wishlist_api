from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.models.users import Users
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.exceptions import ServiceConflictError, ServiceDatabaseError
from app.services.users_service import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_route(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    user = Users(**payload.model_dump())
    try:
        return create_user(db, user)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("", response_model=list[UserRead])
def list_users_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[UserRead]:
    try:
        return list_users(db, skip=skip, limit=limit)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{user_id}", response_model=UserRead)
def get_user_route(user_id: str, db: Session = Depends(get_db)) -> UserRead:
    try:
        user = get_user(db, user_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user_route(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> UserRead:
    try:
        user = get_user(db, user_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        return update_user(db, user)
    except ServiceConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: str, db: Session = Depends(get_db)) -> None:
    try:
        user = get_user(db, user_id)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        delete_user(db, user)
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
