from typing import TypedDict


class TagOut(TypedDict):
    id: int
    name: str
    created_at: str
    updated_at: str


class NoteOut(TypedDict):
    id: int
    title: str
    content: str | None
    is_archived: bool
    created_at: str
    updated_at: str
    tags: list[TagOut]
