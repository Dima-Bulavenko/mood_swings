from uuid import uuid4

from backend.core.domain.mood import CreateMood, Mood, UpdateMood
from backend.core.repository.mood_repository import MoodRepository


class MoodService:
    def __init__(self, mood_repo: MoodRepository) -> None:
        self.mood_repository = mood_repo

    def create_mood(self, data: CreateMood) -> Mood: 
        """Create a new mood record."""
        new_mood = Mood(id=uuid4().hex, user_id=data.user_id, mood=data.mood)
        return self.mood_repository.create(new_mood)

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