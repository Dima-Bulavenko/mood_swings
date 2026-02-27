from sqlalchemy.orm import Session

from core.domain.user import User
from core.repository.user_repository import UserRepository
from infrastructure.sqlalchemy.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(id=model.id)

    @staticmethod
    def _to_model(data: User) -> UserModel:
        return UserModel(id=data.id)

    def create(self, data: User) -> User:
        model = self._to_model(data)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, user_id: str) -> User | None:
        model = self._session.get(UserModel, user_id)
        if model is None:
            return None
        return self._to_domain(model)
