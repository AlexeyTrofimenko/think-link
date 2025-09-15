from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao import notes as notes_dao
from app.db.database import get_session
from app.schemas import NoteCreateSchema, NoteReadSchema, NoteUpdateSchema
from app.services.n8n import note_created_webhook

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteReadSchema, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    background_tasks: BackgroundTasks,
) -> NoteReadSchema:
    note = await notes_dao.create(
        session,
        title=payload.title,
        content=payload.content,
        tags_ids=payload.tags_ids,
    )

    background_tasks.add_task(note_created_webhook, note.id, note.title, note.content)

    return NoteReadSchema.model_validate(note)


@router.get("/", response_model=list[NoteReadSchema], status_code=status.HTTP_200_OK)
async def list_notes(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[NoteReadSchema]:
    rows = await notes_dao.list_all(session)
    return [NoteReadSchema.model_validate(n) for n in rows]


@router.get("/{note_id}", response_model=NoteReadSchema, status_code=status.HTTP_200_OK)
async def get_note(
    note_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteReadSchema:
    note = await notes_dao.get_by_id(session, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteReadSchema.model_validate(note)


@router.patch("/{note_id}", response_model=NoteReadSchema)
async def update_note(
    note_id: int, payload: NoteUpdateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteReadSchema:
    note = await notes_dao.update(
        session,
        note_id,
        title=payload.title,
        content=payload.content,
        is_archived=payload.is_archived,
        tags_ids=payload.tags_ids,
    )
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteReadSchema.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> Response:
    ok = await notes_dao.delete_by_id(session, note_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
