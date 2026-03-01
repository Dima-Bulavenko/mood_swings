from datetime import date

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

	def get_latest_notes(self, limit: int = 5, offset: int = 0) -> list[Note]:
		"""Retrieve latest notes with pagination, including notes of the current user."""
		return self.note_repository.get_latest_notes(limit=limit, offset=offset)
