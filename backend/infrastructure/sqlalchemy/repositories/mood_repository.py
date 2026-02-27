from datetime import date

from sqlalchemy import select
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

    def get_by_user_id_and_date(self, user_id: str, date_create: date) -> Mood | None:
        stmt = select(MoodModel).where(
            MoodModel.user_id == user_id,
            MoodModel.date_create == date_create,
        )
        model = self._session.execute(stmt).scalars().first()
        if model is None:
            return None
        return self._to_domain(model)
