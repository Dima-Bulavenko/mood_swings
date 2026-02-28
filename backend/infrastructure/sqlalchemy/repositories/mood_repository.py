from datetime import date
from typing import cast

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from core.domain.mood import Mood, MoodType
from core.repository.mood_repository import MoodRepository
from infrastructure.sqlalchemy.models import MoodModel


class SQLAlchemyMoodRepository(MoodRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_domain(model: MoodModel) -> Mood:
        return Mood(
            id=model.id,
            user_id=model.user_id,
            mood=MoodType(model.mood),
            date_create=model.date_create,
        )

    @staticmethod
    def _to_model(data: Mood) -> MoodModel:
        return MoodModel(
            id=data.id,
            user_id=data.user_id,
            mood=data.mood.value,
            date_create=data.date_create,
        )

    def create(self, data: Mood) -> Mood:
        model = self._to_model(data)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def create_many(self, data: list[Mood]) -> list[Mood]:
        models = [self._to_model(item) for item in data]
        self._session.add_all(models)
        self._session.commit()
        for model in models:
            self._session.refresh(model)
        return [self._to_domain(model) for model in models]

    def get_by_id(self, mood_id: str) -> Mood | None:
        model = self._session.get(MoodModel, mood_id)
        if model is None:
            return None
        return self._to_domain(model)

    def update(self, data: Mood) -> Mood:
        model = self._session.get(MoodModel, data.id)
        if model is None:
            raise ValueError("Mood record not found.")

        model.user_id = data.user_id
        model.mood = data.mood.value
        model.date_create = data.date_create

        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def get_by_user_id_and_date(self, user_id: str, date_create: date) -> list[Mood]:
        stmt = select(MoodModel).where(
            MoodModel.user_id == user_id,
            MoodModel.date_create == date_create,
        )
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(model) for model in models]

    def delete_by_user_id_and_date(self, user_id: str, date_create: date) -> int:
        stmt = delete(MoodModel).where(
            MoodModel.user_id == user_id,
            MoodModel.date_create == date_create,
        )
        result = cast(CursorResult, self._session.execute(stmt))
        self._session.commit()
        return result.rowcount or 0
    
def get_all_by_user_id(self, user_id: str) -> list[Mood]:
    """Retrieve all mood records for a specific user, sorted by date ascending."""
    stmt = select(MoodModel).where(MoodModel.user_id == user_id).order_by(MoodModel.date_create.asc())
    models = self._session.execute(stmt).scalars().all()
    return [self._to_domain(model) for model in models]

    def get_all_mood_names(self) -> list[str]:
        stmt = select(MoodModel.mood)
        return list(self._session.execute(stmt).scalars().all())

    def get_all_mood_names_with_dates(self) -> list[tuple[date, str]]:
        stmt = select(MoodModel.date_create, MoodModel.mood)
        rows = self._session.execute(stmt).all()
        return [(date_create, mood) for date_create, mood in rows]

    def get_user_mood_names_with_dates(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> list[tuple[date, str]]:
        stmt = select(MoodModel.date_create, MoodModel.mood).where(
            MoodModel.user_id == user_id,
            MoodModel.date_create >= start_date,
            MoodModel.date_create <= end_date,
        )
        rows = self._session.execute(stmt).all()
        return [(date_create, mood) for date_create, mood in rows]
