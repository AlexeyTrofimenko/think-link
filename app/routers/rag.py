from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.note import Note
from app.schemas.rag import (
    AskRequest,
    AskResponse,
    RAGSearchRequest,
    RAGSearchResponse,
    RAGSearchResultItem,
)
from app.services.ollama import answer_with_context, find_relevant_notes_by_cosine

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=RAGSearchResponse, status_code=status.HTTP_200_OK)
async def rag_search(
    payload: RAGSearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RAGSearchResponse:
    rows: list[RAGSearchResultItem] = await find_relevant_notes_by_cosine(
        session=session,
        query_text=payload.query,
        k=payload.top_k,
        max_distance=payload.max_distance,
    )
    return RAGSearchResponse(results=rows)


@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_200_OK)
async def rag_ask(
    payload: AskRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AskResponse:
    relevant_rows: list[RAGSearchResultItem] = await find_relevant_notes_by_cosine(
        session=session,
        query_text=payload.question,
        k=1,
        max_distance=1,
    )
    ids = [r.id for r in relevant_rows]
    rows = []

    if ids:
        content = await session.execute(select(Note.content).where(Note.id.in_(ids)))
        rows = [c for c in content.scalars().all()]

    answer = await answer_with_context(payload.question, rows)

    return AskResponse(answer=answer, used_note_ids=ids)
