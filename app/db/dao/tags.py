from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tag import Tag


async def get_by_id(session: AsyncSession, tag_id: int) -> Tag | None:
    res = await session.execute(select(Tag).where(Tag.id == tag_id))
    return res.scalars().first()


async def get_by_name(session: AsyncSession, name: str) -> Tag | None:
    res = await session.execute(select(Tag).where(Tag.name == name))
    return res.scalars().first()


async def list_all(session: AsyncSession) -> Sequence[Tag]:
    res = await session.execute(select(Tag).order_by(Tag.name.asc()))
    return res.scalars().all()


async def create_or_get(session: AsyncSession, name: str) -> Tag:
    async with session.begin():
        existing = await get_by_name(session, name)
        if existing:
            return existing
        tag = Tag(name=name)
        session.add(tag)

    try:
        await session.refresh(tag)
        return tag
    except IntegrityError:
        await session.rollback()
        again = await get_by_name(session, name)
        if again:
            return again
        raise


async def delete_by_id(session: AsyncSession, tag_id: int) -> bool:
    async with session.begin():
        tag = await get_by_id(session, tag_id)
        if not tag:
            return False
        await session.delete(tag)
    return True
