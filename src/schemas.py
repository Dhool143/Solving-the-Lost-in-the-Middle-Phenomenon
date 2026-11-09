
from typing import Literal

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    score: float
    source: Literal["internal_doc", "web"]


class RAGResponse(BaseModel):
    answer: str
    citations: list[str]
    route_taken: Literal["INTERNAL_RAG", "WEB_FALLBACK"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    transformed_query: str
