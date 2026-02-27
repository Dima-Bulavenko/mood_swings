from collections import Counter
from datetime import date
from typing import List, Tuple

from core.domain.note import Note
from core.repository.note_repository import NoteRepository


class NoteService:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repository = note_repo

    def create(self, note: Note) -> Note:
        """Create and persist a note."""
        return self.note_repository.create(note)

    def get_by_user_id(self, user_id: str) -> list[Note]:
        """Retrieve notes for a specific user."""
        return self.note_repository.get_by_user_id(user_id)

    def get_by_date(self, date: date) -> list[Note]:
        """Retrieve notes for a specific date."""
        return self.note_repository.get_by_date(date)

    def get(self) -> list[Note]:
        """Retrieve all notes."""
        return self.note_repository.get()

    def get_last_five_excluding_user(self, user_id: str) -> list[Note]:
        """Retrieve the latest five notes excluding notes of a specific user."""
        return self.note_repository.get_last_five_excluding_user(user_id)

    def get_top_happy_words(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Analyze all notes and return the top N most common words.
        Returns a list of tuples: (word, frequency)
        """
        all_notes = self.get()
        words = []
        for note in all_notes:
            words.extend(note.note.lower().split())
        counter = Counter(words)
        return counter.most_common(top_n)