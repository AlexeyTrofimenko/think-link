from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas.rag import (
    RAGNote,
    RAGSearchRequest,
    RAGSearchResponse,
)
from app.services.ollama import find_relevant_notes_by_cosine

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=RAGSearchResponse, status_code=status.HTTP_200_OK)
async def rag_search(
    payload: RAGSearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RAGSearchResponse:
    rows: list[RAGNote] = await find_relevant_notes_by_cosine(
        session=session,
        query_text=payload.query,
        k=payload.top_k,
        max_distance=payload.max_distance,
    )
    return RAGSearchResponse(results=rows)
