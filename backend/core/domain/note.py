from datetime import date

from pydantic import BaseModel, Field


class Note(BaseModel):
    user_id: str
    note: str = Field(max_length=100)
    date_create: date = Field(default_factory=date.today)