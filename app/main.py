from fastapi import FastAPI

from app.routers.ai import router as ai_router
from app.routers.health import router as health_router
from app.routers.notes import router as note_router
from app.routers.rag import router as rag_router
from app.routers.tags import router as tag_router

app = FastAPI(title="ThinkLink")

app.include_router(health_router)
app.include_router(note_router)
app.include_router(tag_router)
app.include_router(rag_router)
app.include_router(ai_router)
