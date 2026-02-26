from backend.core.domain.user import User
from backend.core.repository.user_repository import UserRepository
from uuid import uuid4


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self) -> User:
        new_user = User(id=uuid4().hex)
        return self.user_repo.create(new_user)

    def get_user_by_id(self, user_id: str) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        return user