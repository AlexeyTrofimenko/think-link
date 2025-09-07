from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health() -> dict[str, bool]:
    return {"ok": True}


@router.get("/db")
async def health_db(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
    await session.execute(text("select 1"))
    return {"db": "ok"}
