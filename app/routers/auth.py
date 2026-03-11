from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.db import get_db
from app.schemas.auth import Token
from app.schemas.users import UserRead
from app.services.auth_service import authenticate_user, get_current_user
from app.services.exceptions import CredentialsError, ServiceDatabaseError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except CredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except ServiceDatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/user", response_model=UserRead)
async def read_user(current_user = Depends(get_current_user)) -> UserRead:
    return current_user