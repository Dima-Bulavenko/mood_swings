import pandas as pd

from core.domain.analytics import MoodFrequencyChart
from core.repository.mood_repository import MoodRepository


class AnalyticsService:
    def __init__(self, mood_repo: MoodRepository) -> None:
        self.mood_repository = mood_repo

    def get_top_mood_frequency_chart(self, limit: int = 5) -> MoodFrequencyChart:
        """Return chart-friendly payload for most common moods."""
        mood_values = self.mood_repository.get_all_mood_names()
        if not mood_values:
            return MoodFrequencyChart(labels=[], values=[])

        counts = pd.Series(mood_values).value_counts().head(limit)
        records = [(str(label), int(value)) for label, value in counts.items()]

        return MoodFrequencyChart(
            labels=[label for label, _ in records],
            values=[value for _, value in records],
        )
