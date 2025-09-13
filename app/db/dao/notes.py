from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Note, Tag


async def get_by_id(session: AsyncSession, note_id: int) -> Note | None:
    res = await session.execute(
        select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)
    )
    return res.scalars().first()


async def list_all(session: AsyncSession) -> Sequence[Note]:
    res = await session.execute(
        select(Note)
        .options(selectinload(Note.tags))
        .order_by(Note.created_at.desc(), Note.id.desc())
    )
    return res.scalars().all()


async def _load_tags(session: AsyncSession, tags_ids: list[int] | None) -> list[Tag]:
    if not tags_ids:
        return []
    res = await session.execute(select(Tag).where(Tag.id.in_(tags_ids)))
    return list(res.scalars().all())


async def create(
    session: AsyncSession,
    title: str,
    content: str | None,
    tags_ids: list[int] | None = None,
) -> Note:
    async with session.begin():
        note = Note(title=title, content=content)
        note.tags = await _load_tags(session, tags_ids)
        session.add(note)
    await session.refresh(note)
    return note


async def update(
    session: AsyncSession,
    note_id: int,
    title: str | None = None,
    content: str | None = None,
    is_archived: bool | None = None,
    tags_ids: list[int] | None = None,
) -> Note | None:
    async with session.begin():
        res = await session.execute(
            select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)
        )
        note = res.scalars().first()
        if not note:
            return None

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if is_archived is not None:
            note.is_archived = is_archived
        if tags_ids is not None:
            note.tags = await _load_tags(session, tags_ids)

    await session.refresh(note)
    return note


async def delete_by_id(session: AsyncSession, note_id: int) -> bool:
    async with session.begin():
        note = await get_by_id(session, note_id)
        if not note:
            return False
        await session.delete(note)
    return True
