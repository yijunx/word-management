from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.db.models.models import User
from app.schemas.pagination import ResponsePagination, QueryPagination
from app.schemas.user import UserInContribution


class DialectEnum(str, Enum):
    anyhua = ""
    hangzhouhua = "杭州话"
    guangdonghua = "广东话"


class WordCreate(BaseModel):

    title: str
    explanation: str  # well you cannot submit without give explanation..
    pronunciation: Optional[str]
    usage: Optional[str]
    tags: List[str]
    dialect: DialectEnum


class WordPatch(BaseModel):
    # well only title can be updated...
    title: str


class WordMerge(BaseModel):
    word_id_to_merge_into: str


class Word(BaseModel):
    id: str  # this user id is from token in cookie
    title: str

    locked: bool
    merged_to: Optional[str]
    dialect: str

    created_at: datetime
    modified_at: datetime
    created_by: str

    merged_by: Optional[str]
    merged_at: Optional[datetime]

    locked_by: Optional[str]
    deactivated_by: Optional[str]

    class Config:
        orm_mode = True


class WordWithFields(Word):
    explanation: Optional[str]
    pronunciation: Optional[str]
    usage: Optional[str]
    tags: List[str] = []

    # class Config:
    #     orm_mode = True


class WordWithFieldsWithPaging(BaseModel):
    data: List[WordWithFields]
    paging: ResponsePagination


class WordQuery(QueryPagination):
    tag: Optional[str]
    title: Optional[str]
    dialect: Optional[DialectEnum]


class WordContribution(BaseModel):
    data: List[UserInContribution]
