from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Note(BaseModel):
    user_id: str
    note: str = Field(max_length=100)
    date_create: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))