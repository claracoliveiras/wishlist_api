import uuid

from sqlalchemy import UUID, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_picture: Mapped[str] = mapped_column(Text, nullable=True)
    banner_picture: Mapped[str] = mapped_column(Text, nullable=True)
