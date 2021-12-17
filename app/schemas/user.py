from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    # user will (must) have profile picture in the future
    id: str  # this user id is from token in cookie
    name: str
    email: str

    # admin info
    is_word_admin: bool = False
    is_field_version_admin: bool = False
    is_suggestion_admin: bool = False

    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    """used for internally update the name or email"""
    name: Optional[str]
    email: Optional[str]


class UserInContribution(BaseModel):
    """here i dont want to specify who contribute more or less
    nor i want to specify who is word creator, or version creator, or who supports with suggetions"""

    id: str
    name: str

    class Config:
        orm_mode = True
