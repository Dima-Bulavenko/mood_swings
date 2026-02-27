from abc import ABC, abstractmethod

from core.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, data: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        pass