from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.tag import Tag
from app.schemas.tag import TagCreateSchema, TagReadSchema

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagReadSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TagCreateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> TagReadSchema:
    existing = await session.scalar(select(Tag).where(Tag.name == payload.name))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")

    tag = Tag(name=payload.name)

    async with session.begin():
        session.add(tag)

    await session.refresh(tag)
    return TagReadSchema.model_validate(tag)


@router.get("/", response_model=list[TagReadSchema], status_code=status.HTTP_200_OK)
async def list_tags(session: Annotated[AsyncSession, Depends(get_session)]) -> list[TagReadSchema]:
    rows = (await session.execute(select(Tag).order_by(Tag.name.asc()))).scalars().all()
    return [TagReadSchema.model_validate(t) for t in rows]


@router.get("/{tag_id}", response_model=TagReadSchema, status_code=status.HTTP_200_OK)
async def get_tag(
    tag_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> TagReadSchema:
    tag = await session.scalar(select(Tag).where(Tag.id == tag_id))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return TagReadSchema.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
    tag = await session.scalar(select(Tag).where(Tag.id == tag_id))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    async with session.begin():
        await session.delete(tag)
    return None
