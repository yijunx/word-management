from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.schemas.pagination import ResponsePagination, QueryPagination


class DialectEnum(str, Enum):
    hangzhouhua = "杭州话"
    guangdonghua = "广东话"


class WordCreate(BaseModel):

    title: str
    explanation: str  # well you cannot submit without give explanation..
    pronunciation: Optional[str]
    usage: Optional[str]
    tags: Optional[str]
    dialect: DialectEnum


class Word(BaseModel):
    id: str  # this user id is from token in cookie

    locked: bool
    merged_to: str
    dialect: str

    created_at: datetime
    modified_at: datetime
    created_by: str

    class Config:
        orm_mode = True


class WordWithFields(Word):
    explanation: Optional[str]
    pronunciation: Optional[str]
    usage: Optional[str]
    tags: Optional[str]


class WordWithFieldsWithPaging(BaseModel):
    data: List[WordWithFields]
    paging: ResponsePagination


class WordQueryByTitle(QueryPagination):
    title: Optional[str]
    dialect: Optional[DialectEnum]


class WordQueryByTag(QueryPagination):
    tag: str
    dialect: Optional[DialectEnum]
