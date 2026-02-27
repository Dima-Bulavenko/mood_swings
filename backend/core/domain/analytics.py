from pydantic import BaseModel


class MoodFrequencyChart(BaseModel):
    labels: list[str]
    values: list[int]


class WeeklyPopularMoodChart(BaseModel):
    labels: list[str]
    moods: list[str]
    values: list[int]
