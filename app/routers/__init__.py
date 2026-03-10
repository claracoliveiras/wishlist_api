from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.routers.collections import router as collections_router
from app.routers.collection_items import router as collection_items_router
from app.routers.following import router as following_router

__all__ = [
    "users_router",
    "items_router",
    "collections_router",
    "collection_items_router",
    "following_router",
]
