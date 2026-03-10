import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CollectionItems(Base):
    __tablename__ = "collection_items"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    collection_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collections.id", ondelete="CASCADE"))