from pydantic import BaseModel


class NoteAgentRequest(BaseModel):
    message: str


class NoteAgentResponse(BaseModel):
    answer: str | None = None
    note_id: int | None = None
