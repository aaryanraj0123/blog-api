from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime | None
    votes: int

    class Config:
        from_attributes = True