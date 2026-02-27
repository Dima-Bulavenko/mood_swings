from abc import ABC, abstractmethod
from datetime import date

from core.domain.note import Note


class NoteRepository(ABC):
    @abstractmethod
    def create(self, note: Note) -> Note:
        """Create and persist a note."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[Note]:
        """Retrieve notes for a specific user."""
        pass

    @abstractmethod
    def get_by_date(self, date: date) -> list[Note]:
        """Retrieve notes for a specific date."""
        pass

    @abstractmethod
    def get(self) -> list[Note]:
        """Retrieve all notes."""
        pass

    @abstractmethod
    def get_last_five_excluding_user(self, user_id: str) -> list[Note]:
        """Retrieve the latest five notes excluding notes created by the provided user."""
        pass