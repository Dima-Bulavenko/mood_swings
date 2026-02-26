from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from core.domain.note import Note


class NoteRepository(ABC):
    @abstractmethod
    def create(self, note: Note) -> Note:
        """Create and persist a note."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> list[Note]:
        """Retrieve notes for a specific user."""
        pass

    @abstractmethod
    def get_by_date(self, date: datetime) -> list[Note]:
        """Retrieve notes for a specific date."""
        pass

    @abstractmethod
    def get(self) -> list[Note]:
        """Retrieve all notes."""
        pass