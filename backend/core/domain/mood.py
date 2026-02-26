from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class MoodType(str, Enum):
    JOYFUL = "joyful"
    GRATEFUL = "grateful"
    EXCITED = "excited"
    PROUD = "proud"
    PEACEFUL = "peaceful"
    HAPPY = "happy"

    TIRED = "tired"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    OVERWHELMED = "overwhelmed"
    LOST = "lost"
    SPIRALLING = "spiralling"

    SAD = "sad"
    LONELY = "lonely"
    MEH = "meh"
    HURT = "hurt"
    BROKEN_HEARTED = "broken-hearted"
    UNMOTIVATED = "unmotivated"
    DEJECTED = "dejected"


class Mood(BaseModel):
    id: str
    user_id: str
    mood: MoodType
    date_create: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CreateMood(BaseModel):
    user_id: str
    mood: MoodType


class UpdateMood(BaseModel):
    id: str
    mood: MoodType
