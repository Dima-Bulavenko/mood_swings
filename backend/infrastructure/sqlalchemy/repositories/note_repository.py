from datetime import date

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from core.domain.note import Note
from core.repository.note_repository import NoteRepository
from infrastructure.sqlalchemy.models import NoteModel


class SQLAlchemyNoteRepository(NoteRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_domain(model: NoteModel) -> Note:
        return Note(
            id=model.id,
            user_id=model.user_id,
            note=model.note,
            date_create=model.date_create,
        )

    @staticmethod
    def _to_model(data: Note) -> NoteModel:
        return NoteModel(
            id=data.id,
            user_id=data.user_id,
            note=data.note,
            date_create=data.date_create,
        )

    def create(self, note: Note) -> Note:
        model = self._to_model(note)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def get_by_user_id(self, user_id: str) -> list[Note]:
        stmt = select(NoteModel).where(NoteModel.user_id == user_id)
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def get_by_date(self, date: date) -> list[Note]:
        stmt = select(NoteModel).where(NoteModel.date_create == date)
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def get(self) -> list[Note]:
        stmt = select(NoteModel)
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def get_latest_notes(self, limit: int = 5, offset: int = 0) -> list[Note]:
        stmt = (
            select(NoteModel)
            .order_by(desc(NoteModel.date_create), desc(NoteModel.id))
            .offset(offset)
            .limit(limit)
        )
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def get_all_note_texts(self) -> list[str]:
        stmt = select(NoteModel.note)
        return list(self._session.execute(stmt).scalars().all())
