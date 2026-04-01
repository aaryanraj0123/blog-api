from pydantic import BaseModel
from uuid import UUID
from typing import Literal

class VoteRequest(BaseModel):
    post_id: UUID
    vote: int
    