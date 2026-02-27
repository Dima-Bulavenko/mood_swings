from datetime import date
from uuid import uuid4
from collections import Counter

from core.domain.mood import CreateMood, Mood, MoodType, UpdateMood
from core.repository.mood_repository import MoodRepository


class MoodService:
    def __init__(self, mood_repo: MoodRepository) -> None:
        self.mood_repository = mood_repo

    def create_mood(self, data: CreateMood) -> Mood: 
        """Create a new mood record."""
        new_mood = Mood(id=uuid4().hex, user_id=data.user_id, mood=data.mood)
        return self.mood_repository.create(new_mood)

    def create_moods(self, user_id: str, moods: list[MoodType]) -> list[Mood]:
        """Create multiple mood records for a user."""
        mood_records = [Mood(id=uuid4().hex, user_id=user_id, mood=mood) for mood in moods]
        return self.mood_repository.create_many(mood_records)

    def get_mood_by_id(self, mood_id: str) -> Mood:
        """Retrieve a mood by its identifier."""
        mood = self.mood_repository.get_by_id(mood_id)
        if mood is None:
            raise ValueError("Mood record not found.")
        return mood

    def update_mood(self, data: UpdateMood):
        """Update an existing mood record."""
        old_mood = self.mood_repository.get_by_id(data.id)
        if not old_mood:
            raise ValueError("Mood record not found.")
        old_mood.mood = data.mood
        return self.mood_repository.update(old_mood)

    def get_todays_moods_by_user_id(self, user_id: str) -> list[Mood]:
        """Retrieve all today's moods for a specific user."""
        moods = self.mood_repository.get_by_user_id_and_date(user_id=user_id, date_create=date.today())
        if not moods:
            raise ValueError("Mood record not found.")
        return moods

    def update_todays_moods_by_user_id(self, user_id: str, moods: list[MoodType]) -> list[Mood]:
        """Replace all today's moods for a specific user."""
        existing_moods = self.mood_repository.get_by_user_id_and_date(
            user_id=user_id,
            date_create=date.today(),
        )
        if not existing_moods:
            raise ValueError("Mood record not found.")

        self.mood_repository.delete_by_user_id_and_date(user_id=user_id, date_create=date.today())
        mood_records = [Mood(id=uuid4().hex, user_id=user_id, mood=mood) for mood in moods]
        return self.mood_repository.create_many(mood_records)

    def get_user_history(self, user_id: str) -> list[Mood]:
        """Return all mood records for a specific user, sorted by date."""
        return self.mood_repository.get_all_by_user_id(user_id)