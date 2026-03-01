from datetime import date, timedelta

import pandas as pd

from core.domain.analytics import MoodFrequencyChart, TopHappyWordsChart, UserMoodHistoryChart, WeeklyPopularMoodChart
from core.repository.mood_repository import MoodRepository
from core.repository.note_repository import NoteRepository


class AnalyticsService:
    def __init__(self, mood_repo: MoodRepository, note_repo: NoteRepository) -> None:
        self.mood_repository = mood_repo
        self.note_repository = note_repo

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

    def get_top_happy_words_chart(self, limit: int = 10) -> TopHappyWordsChart:
        """Return top common words from users' happiness notes."""
        note_texts = self.note_repository.get_all_note_texts()
        if not note_texts:
            return TopHappyWordsChart(labels=[], values=[])

        stopwords = {
            "a",
            "an",
            "the",
            "with",
            "my",
            "and",
            "of",
            "for",
            "to",
            "in",
            "on",
            "at",
            "is",
            "it",
            "was",
            "had",
            "this",
            "that",
            "from",
            "got",
            "day",
            "today",
            "me",
            "really",
            "so",
            "time",
            "received",
            "something",
            "about",
        }

        words_series = (
            pd.Series(note_texts)
            .dropna()
            .astype(str)
            .str.lower()
            .str.replace(r"[^a-zA-Z0-9\s]", " ", regex=True)
            .str.split()
            .explode()
        )

        filtered_words = words_series[
            words_series.notna()
            & (words_series.str.len() > 1)
            & (~words_series.isin(stopwords))
        ]

        counts = filtered_words.value_counts().head(limit)
        records = [(str(label), int(value)) for label, value in counts.items()]

        return TopHappyWordsChart(
            labels=[label for label, _ in records],
            values=[value for _, value in records],
        )

    def get_user_mood_history_chart(self, user_id: str, days: int = 7) -> UserMoodHistoryChart:
        """Return user's mood history for the last N days with gaps as null."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        mood_rows = self.mood_repository.get_user_mood_names_with_dates(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        date_index = pd.date_range(start=start_date, end=end_date, freq="D")
        labels = [day.strftime("%Y-%m-%d") for day in date_index]

        if not mood_rows:
            return UserMoodHistoryChart(labels=labels, moods=[None] * len(labels))

        df = pd.DataFrame(mood_rows, columns=["date_create", "mood"])
        df["date_create"] = pd.to_datetime(df["date_create"])

        daily = (
            df.groupby(["date_create", "mood"]).size().reset_index(name="count")
            .sort_values(["date_create", "count", "mood"], ascending=[True, False, True])
            .drop_duplicates(subset=["date_create"], keep="first")
            .set_index("date_create")
        )

        daily = daily.reindex(date_index)
        moods = [str(value) if pd.notna(value) else None for value in daily["mood"].tolist()]

        return UserMoodHistoryChart(labels=labels, moods=moods)
