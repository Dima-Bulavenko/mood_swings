from abc import ABC, abstractmethod

from core.domain.mood import Mood


class MoodRepository(ABC):
    @abstractmethod
    def create(self, data: Mood) -> Mood:
        """Create and persist a mood record."""
        pass

    @abstractmethod
    def get_by_id(self, mood_id: str) -> Mood | None:
        """Retrieve a mood by its identifier."""
        pass

    @abstractmethod
    def update(self, data: Mood) -> Mood:
        """Update an existing mood record."""
        pass