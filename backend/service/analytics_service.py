import pandas as pd

from core.domain.analytics import MoodFrequencyChart, WeeklyPopularMoodChart
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

    def get_weekly_popular_mood_chart(self) -> WeeklyPopularMoodChart:
        """Return the most popular mood for each day of the week."""
        mood_rows = self.mood_repository.get_all_mood_names_with_dates()
        if not mood_rows:
            return WeeklyPopularMoodChart(labels=[], moods=[], values=[])

        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        df = pd.DataFrame(mood_rows, columns=["date_create", "mood"])
        df["day_of_week"] = pd.to_datetime(df["date_create"]).dt.day_name()

        grouped = df.groupby(["day_of_week", "mood"]).size().reset_index(name="count")
        grouped["day_of_week"] = pd.Categorical(grouped["day_of_week"], categories=days_order, ordered=True)

        top_per_day = grouped.sort_values(
            ["day_of_week", "count", "mood"],
            ascending=[True, False, True],
        ).drop_duplicates(subset=["day_of_week"], keep="first")

        labels = top_per_day["day_of_week"].astype(str).tolist()
        moods = top_per_day["mood"].astype(str).tolist()
        values = top_per_day["count"].astype(int).tolist()

        return WeeklyPopularMoodChart(labels=labels, moods=moods, values=values)
