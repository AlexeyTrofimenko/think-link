from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao import tags as tags_dao
from app.db.database import get_session
from app.schemas.tag import TagCreateSchema, TagReadSchema

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagReadSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TagCreateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> TagReadSchema:
    tag = await tags_dao.create_or_get(session, payload.name)
    return TagReadSchema.model_validate(tag)


@router.get("/", response_model=list[TagReadSchema], status_code=status.HTTP_200_OK)
async def list_tags(session: Annotated[AsyncSession, Depends(get_session)]) -> list[TagReadSchema]:
    rows = await tags_dao.list_all(session)
    return [TagReadSchema.model_validate(t) for t in rows]


@router.get("/{tag_id}", response_model=TagReadSchema, status_code=status.HTTP_200_OK)
async def get_tag(
    tag_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> TagReadSchema:
    tag = await tags_dao.get_by_id(session, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return TagReadSchema.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> Response:
    ok = await tags_dao.delete_by_id(session, tag_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
