from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class Note(BaseModel):
    user_id: UUID
    note: str = Field(max_length=100)
    date_create: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))