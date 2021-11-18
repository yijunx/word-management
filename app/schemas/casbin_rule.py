from pydantic import BaseModel
from typing import List, Optional
from app.casbin.role_definition import PolicyTypeEnum
from app.schemas.pagination import ResponsePagination


class CasbinRule(BaseModel):
    ptype: PolicyTypeEnum
    v0: Optional[str]
    v1: Optional[str]
    v2: Optional[str]
    v3: Optional[str]
    v4: Optional[str]
    v5: Optional[str]

    class Config:
        orm_mode = True


class CasbinRuleWithPaging(BaseModel):
    data: List[CasbinRule]
    paging: ResponsePagination


class CasbinRulePatch(BaseModel):
    ptype: PolicyTypeEnum
    v0: Optional[str]
    v1: Optional[str]
    v2: Optional[str]
