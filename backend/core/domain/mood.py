from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class MoodType(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    ANXIOUS = "anxious"
    EXCITED = "excited"


class Mood(BaseModel):
    user_id: UUID
    mood: MoodType
    date_create: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))