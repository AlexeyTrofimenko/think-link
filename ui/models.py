from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TagReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class NoteReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagReadSchema] = []


class NoteAgentRequest(BaseModel):
    message: str


class NoteAgentResponse(BaseModel):
    answer: str | None = None
    note_id: int | None = None


class SelectedNoteAgentRequest(BaseModel):
    note_id: int
    message: str
