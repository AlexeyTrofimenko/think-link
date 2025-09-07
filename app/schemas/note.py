from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tag import TagReadSchema


class NoteCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str | None = None
    tags_ids: list[int] = []


class NoteReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagReadSchema] = []


class NoteUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None
    is_archived: bool | None = None
    tag_ids: list[int] | None = None
