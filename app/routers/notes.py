from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models import Note, Tag
from app.schemas import NoteCreateSchema, NoteReadSchema, NoteUpdateSchema

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteReadSchema, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteReadSchema:
    async with session.begin():
        note = Note(title=payload.title, content=payload.content)
        if payload.tags_ids:
            tags = list(
                (await session.execute(select(Tag).where(Tag.id.in_(payload.tags_ids))))
                .scalars()
                .all()
            )
            note.tags = tags
        session.add(note)
    await session.refresh(note)
    return NoteReadSchema.model_validate(note)


@router.get("/", response_model=list[NoteReadSchema], status_code=status.HTTP_200_OK)
async def list_notes(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[NoteReadSchema]:
    rows = (await session.execute(select(Note).order_by(Note.created_at.desc()))).scalars().all()
    return [NoteReadSchema.model_validate(n) for n in rows]


@router.get("/{note_id}", response_model=NoteReadSchema, status_code=status.HTTP_200_OK)
async def get_note(
    note_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteReadSchema:
    note = await session.scalar(select(Note).where(Note.id == note_id))
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteReadSchema.model_validate(note)


@router.patch("/{note_id}", response_model=NoteReadSchema)
async def update_note(
    note_id: int, payload: NoteUpdateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> NoteReadSchema:
    async with session.begin():
        note = await session.scalar(select(Note).where(Note.id == note_id))
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if payload.title is not None:
            note.title = payload.title
        if payload.content is not None:
            note.content = payload.content
        if payload.is_archived is not None:
            note.is_archived = payload.is_archived
        if payload.tag_ids is not None:
            tags = list(
                (await session.execute(select(Tag).where(Tag.id.in_(payload.tag_ids))))
                .scalars()
                .all()
            )
            note.tags = tags

    await session.refresh(note)
    return NoteReadSchema.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> Response:
    async with session.begin():
        note = await session.scalar(select(Note).where(Note.id == note_id))
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        await session.delete(note)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
