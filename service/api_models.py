from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class SourceResponse(BaseModel):
    title: str
    source: str
    chunk_index: int
    content_type: str
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]


class StatsResponse(BaseModel):
    documents_count: int
    images_count: int
    chunk_count: int
    indexed_chunk_count: int