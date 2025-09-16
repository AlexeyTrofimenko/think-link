from pydantic import BaseModel


class RAGSearchRequest(BaseModel):
    query: str
    top_k: int
    max_distance: float | None


class RAGSearchResultItem(BaseModel):
    id: int
    distance: float


class RAGSearchResponse(BaseModel):
    results: list[RAGSearchResultItem]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    used_note_ids: list[int]
