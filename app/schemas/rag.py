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
