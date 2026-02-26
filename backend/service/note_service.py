from datetime import datetime

from backend.core.domain.note import Note
from backend.core.repository.note_repository import NoteRepository


class NoteService:
	def __init__(self, note_repo: NoteRepository) -> None:
		self.note_repository = note_repo

	def create(self, note: Note) -> Note:
		"""Create and persist a note."""
		return self.note_repository.create(note)

	def get_by_user_id(self, user_id: str) -> list[Note]:
		"""Retrieve notes for a specific user."""
		return self.note_repository.get_by_user_id(user_id)

	def get_by_date(self, date: datetime) -> list[Note]:
		"""Retrieve notes for a specific date."""
		return self.note_repository.get_by_date(date)

	def get(self) -> list[Note]:
		"""Retrieve all notes."""
		return self.note_repository.get()
