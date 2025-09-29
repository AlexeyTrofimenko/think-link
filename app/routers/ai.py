from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.note_agent import Answer as NoteAnswer
from app.ai.note_agent import NoteDeps, UpdatedNote
from app.ai.note_agent import agent as note_agent
from app.ai.notes_agent import Answer, CreatedNote, DBDeps
from app.ai.notes_agent import agent as notes_agent
from app.db.dao.notes import get_by_id
from app.db.database import get_session
from app.schemas.agents import NoteAgentRequest, NoteAgentResponse, SelectedNoteAgentRequest
from app.services.n8n import note_created_webhook
from app.services.ollama import compute_note_embedding

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/ask", response_model=NoteAgentResponse, status_code=status.HTTP_200_OK)
async def rag_ask(
    payload: NoteAgentRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    background_tasks: BackgroundTasks,
) -> NoteAgentResponse:
    deps = DBDeps(session=session)
    result = await notes_agent.run(payload.message, deps=deps)

    if isinstance(result.output, CreatedNote):
        note = await get_by_id(session, result.output.note_id)

        background_tasks.add_task(note_created_webhook, note.id, note.title, note.content)
        background_tasks.add_task(compute_note_embedding, note.id, note.content)

        return NoteAgentResponse(note_id=result.output.note_id)
    elif isinstance(result.output, Answer):
        return NoteAgentResponse(answer=result.output.answer)
    return NoteAgentResponse(answer="Sorry, I couldn't process that.")


@router.post("/do", response_model=NoteAgentResponse, status_code=status.HTTP_200_OK)
async def note_ask(
    payload: SelectedNoteAgentRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    background_tasks: BackgroundTasks,
) -> NoteAgentResponse:
    note = await get_by_id(session, payload.note_id)

    if not note:
        return NoteAgentResponse(answer=f"Note {payload.note_id} not found")

    composed_message = (
        f"Current note:\n"
        f"Title: {note.title}\n"
        f"Content:\n{note.content or ''}\n\n"
        f"User request:\n{payload.message}"
    )

    deps = NoteDeps(session=session, note_id=note.id)
    result = await note_agent.run(composed_message, deps=deps)

    if isinstance(result.output, UpdatedNote):
        background_tasks.add_task(note_created_webhook, note.id, note.title, note.content)
        background_tasks.add_task(compute_note_embedding, note.id, note.content)

        return NoteAgentResponse(note_id=result.output.note_id)
    elif isinstance(result.output, NoteAnswer):
        return NoteAgentResponse(answer=result.output.answer)
    return NoteAgentResponse(answer=f"Sorry, I couldn't process that. {result.output}")
