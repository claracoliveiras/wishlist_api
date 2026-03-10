from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    profile_picture: Mapped[str] = mapped_column(Text, nullable=True)
    banner_picture: Mapped[str] = mapped_column(Text, nullable=True)