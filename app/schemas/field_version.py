from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.schemas.pagination import ResponsePagination, QueryPagination


class ContentPatch(BaseModel):
    content: str


class FieldEnum(str, Enum):
    explanation = "explanation"
    usage = "usage"
    tags = "tags"
    pronunciation = "pronunciation"


class FieldVersionCreate(BaseModel):

    word_id: str
    field: FieldEnum
    content: str


class FieldVersion(FieldVersionCreate):

    id: str

    created_at: datetime
    modified_at: datetime
    created_by: str

    up_votes: int
    down_votes: int

    class Config:
        orm_mode = True


class FieldVersionWithPaging(BaseModel):
    data: List[FieldVersion]
    paging: ResponsePagination
