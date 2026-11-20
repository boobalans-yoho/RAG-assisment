
from pydantic import BaseModel, Field
from typing import Any


class Source(BaseModel):
    id: str
    text: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=20)
    filters: dict[str, Any] = Field(default_factory=dict)


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source] = Field(default_factory=list)
    fallback: bool = False


class SearchRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=20)
    filters: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    results: list[Source] = Field(default_factory=list)
