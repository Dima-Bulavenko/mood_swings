from abc import ABC, abstractmethod
from datetime import date

from core.domain.mood import Mood


class MoodRepository(ABC):
    @abstractmethod
    def create(self, data: Mood) -> Mood:
        """Create and persist a mood record."""
        pass

    @abstractmethod
    def create_many(self, data: list[Mood]) -> list[Mood]:
        """Create and persist multiple mood records."""
        pass

    @abstractmethod
    def get_by_id(self, mood_id: str) -> Mood | None:
        """Retrieve a mood by its identifier."""
        pass

    @abstractmethod
    def update(self, data: Mood) -> Mood:
        """Update an existing mood record."""
        pass

    @abstractmethod
    def get_by_user_id_and_date(self, user_id: str, date_create: date) -> list[Mood]:
        """Retrieve all moods for a user on a specific date."""
        pass

    @abstractmethod
    def delete_by_user_id_and_date(self, user_id: str, date_create: date) -> int:
        """Delete all moods for a user on a specific date and return deleted count."""
        pass

    @abstractmethod
    def get_all_mood_names(self) -> list[str]:
        """Retrieve all mood names only."""
        pass