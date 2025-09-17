from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.notes_agent import Answer, CreatedNote, DBDeps, agent
from app.db.database import get_session
from app.schemas.agents import NoteAgentRequest, NoteAgentResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/ask", response_model=NoteAgentResponse, status_code=status.HTTP_200_OK)
async def rag_ask(
    payload: NoteAgentRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NoteAgentResponse:
    deps = DBDeps(session=session)
    result = await agent.run(payload.message, deps=deps)

    if isinstance(result.output, CreatedNote):
        return NoteAgentResponse(note_id=result.output.note_id)
    elif isinstance(result.output, Answer):
        return NoteAgentResponse(answer=result.output.answer)
    return NoteAgentResponse(answer="Sorry, I couldn't process that.")
