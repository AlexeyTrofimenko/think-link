from pydantic import BaseModel


class RAGNote(BaseModel):
    id: int
    title: str
    content: str


class RAGSearchRequest(BaseModel):
    query: str
    top_k: int
    max_distance: float | None


class RAGSearchResponse(BaseModel):
    results: list[RAGNote]
