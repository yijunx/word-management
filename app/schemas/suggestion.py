from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.schemas.pagination import ResponsePagination, QueryPagination


class SuggestionCreate(BaseModel):

    word_id: str
    version_id: str
    content: str


class Suggestion(SuggestionCreate):
    id: str

    created_at: datetime
    modified_at: datetime
    created_by: str
    accepted: bool


class SuggestionWithPaging(BaseModel):
    data: List[Suggestion]
    paging: ResponsePagination


class SuggestionQuery(QueryPagination):
    word_id: str
    version_id: Optional[str]
