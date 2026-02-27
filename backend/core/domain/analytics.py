from pydantic import BaseModel


class MoodFrequencyChart(BaseModel):
    labels: list[str]
    values: list[int]
