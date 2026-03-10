from fastapi import FastAPI

from app.routers.collection_items import router as collection_items_router
from app.routers.collections import router as collections_router
from app.routers.following import router as following_router
from app.routers.items import router as items_router
from app.routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(items_router)
app.include_router(collections_router)
app.include_router(collection_items_router)
app.include_router(following_router)


@app.get("/")
async def health() -> dict[str, str]:
    return {"message": "Ok!"}
