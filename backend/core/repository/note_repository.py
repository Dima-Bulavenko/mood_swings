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
    def get_latest_notes(self, limit: int = 5, offset: int = 0) -> list[Note]:
        """Retrieve latest notes with pagination, including notes by any user."""
        pass

    @abstractmethod
    def get_all_note_texts(self) -> list[str]:
        """Retrieve all note texts only."""
        pass