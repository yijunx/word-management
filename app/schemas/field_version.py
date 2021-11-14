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
    """there is word_id in the payload
    so there is no need to have word_id in the path"""

    word_id: str
    field: FieldEnum
    content: str


class FieldVersionPatch(BaseModel):
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


class FieldVersionQuery(QueryPagination):
    """word id optional"""

    word_id: Optional[str]
    field: Optional[FieldEnum]
