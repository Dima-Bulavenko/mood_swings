from sqlalchemy import Date, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	__tablename__ = "users"

	id: Mapped[str] = mapped_column(String, primary_key=True)


class MoodModel(Base):
	__tablename__ = "moods"

	id: Mapped[str] = mapped_column(String, primary_key=True)
	user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
	mood: Mapped[str] = mapped_column(String, nullable=False)
	date_create: Mapped[Date] = mapped_column(Date, nullable=False)


class NoteModel(Base):
	__tablename__ = "notes"

	id: Mapped[str] = mapped_column(String, primary_key=True)
	user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
	note: Mapped[str] = mapped_column(String(100), nullable=False)
	date_create: Mapped[Date] = mapped_column(Date, nullable=False)
