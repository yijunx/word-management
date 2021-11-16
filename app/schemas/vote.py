from pydantic import BaseModel
from datetime import datetime


class VoteCreate(BaseModel):
    vote_up: bool


class Vote(VoteCreate):
    id: str

    version_id: str
    created_by: str
    created_at: datetime
