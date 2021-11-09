from pydantic import BaseModel


class User(BaseModel):
    id: str  # this user id is from token in cookie
    name: str
    email: str

    class Config:
        orm_mode = True
