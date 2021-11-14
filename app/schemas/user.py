from pydantic import BaseModel


class User(BaseModel):
    # user will (must) have profile picture in the future
    id: str  # this user id is from token in cookie
    name: str
    email: str

    class Config:
        orm_mode = True


class UserInContribution(BaseModel):
    """here i dont want to specify who contribute more or less
    nor i want to specify who is word creator, or version creator, or who supports with suggetions"""

    id: str
    name: str

    class Config:
        orm_mode = True
