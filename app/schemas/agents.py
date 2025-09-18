from pydantic import BaseModel


class NoteAgentRequest(BaseModel):
    message: str


class NoteAgentResponse(BaseModel):
    answer: str | None = None
    note_id: int | None = None


class SelectedNoteAgentRequest(BaseModel):
    note_id: int
    message: str
