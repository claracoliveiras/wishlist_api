import uuid

from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Items(Base):
    __tablename__ = "items"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    item_url: Mapped[str] = mapped_column(Text, nullable=False)
    item_img: Mapped[str] = mapped_column(Text, nullable=False)