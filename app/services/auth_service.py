from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.db.db import get_db
from app.schemas.auth import TokenData
from app.services.exceptions import CredentialsError, ServiceDatabaseError
from app.services.users_service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

DUMMY_HASH = get_password_hash(settings.dummy_hash_input)


def authenticate_user(db: Session, username: str, password: str):
    try:
        user = get_user_by_username(db, username)
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to load user for authentication") from exc

    if not user:
        verify_password(password, DUMMY_HASH)
        raise CredentialsError("Could not validate credentials")

    if not verify_password(password, user.password):
        raise CredentialsError("Could not validate credentials")

    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except jwt.InvalidTokenError as exc:
        raise CredentialsError("Could not validate credentials") from exc
    
    payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

    username = payload.get("sub")
    if username is None:
        raise CredentialsError("Could not validate credentials")

    token_data = TokenData(username=username)

    try:
        user = get_user_by_username(db, username=token_data.username)
    except SQLAlchemyError as exc:
        db.rollback()
        raise ServiceDatabaseError("Failed to load current user") from exc

    if user is None:
        raise CredentialsError("Could not validate credentials")

    return user
