from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.domain.mood import CreateMood, Mood, MoodType
from core.domain.note import Note
from core.domain.user import User
from infrastructure.sqlalchemy.models import Base
from infrastructure.sqlalchemy.repositories.mood_repository import SQLAlchemyMoodRepository
from infrastructure.sqlalchemy.repositories.note_repository import SQLAlchemyNoteRepository
from infrastructure.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository
from service.mood_service import MoodService
from service.note_service import NoteService
from service.user_service import UserService


DATABASE_URL = "sqlite:///./mood_swings.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
	Base.metadata.create_all(bind=engine)
	yield


app = FastAPI(lifespan=lifespan)


class CreateMoodRequest(BaseModel):
	mood: MoodType


class UpdateMoodRequest(BaseModel):
	mood: MoodType


class CreateNoteRequest(BaseModel):
	note: str = Field(max_length=100)


class ErrorResponse(BaseModel):
	detail: str


def get_session() -> Generator[Session, None, None]:
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()


def get_user_service(session: Session = Depends(get_session)) -> UserService:
	repository = SQLAlchemyUserRepository(session)
	return UserService(repository)


def get_mood_service(session: Session = Depends(get_session)) -> MoodService:
	repository = SQLAlchemyMoodRepository(session)
	return MoodService(repository)


def get_note_service(session: Session = Depends(get_session)) -> NoteService:
	repository = SQLAlchemyNoteRepository(session)
	return NoteService(repository)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user_service: UserService = Depends(get_user_service)) -> User:
	"""Create a new user and return the generated user identifier."""
	return user_service.create_user()


@app.post("/moods", response_model=Mood, status_code=status.HTTP_201_CREATED, tags=["moods"])
def create_mood(
	request: CreateMoodRequest,
	user_id: str,
	mood_service: MoodService = Depends(get_mood_service),
) -> Mood:
	"""Create today's mood entry for the user provided via query parameter."""
	return mood_service.create_mood(CreateMood(user_id=user_id, mood=request.mood))


@app.get(
	"/moods/today",
	response_model=Mood,
	tags=["moods"],
	responses={
		404: {
			"model": ErrorResponse,
			"description": "Mood for today was not found for the provided user.",
		},
	},
)
def get_todays_mood(
	user_id: str,
	mood_service: MoodService = Depends(get_mood_service),
) -> Mood:
	"""Retrieve today's mood for the user provided via query parameter."""
	try:
		return mood_service.get_todays_mood_by_user_id(user_id)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.put(
	"/moods/today",
	response_model=Mood,
	tags=["moods"],
	responses={
		404: {
			"model": ErrorResponse,
			"description": "Mood for today was not found for the provided user.",
		},
	},
)
def update_todays_mood(
	request: UpdateMoodRequest,
	user_id: str,
	mood_service: MoodService = Depends(get_mood_service),
) -> Mood:
	"""Update today's mood for the user provided via query parameter."""
	try:
		return mood_service.update_todays_mood_by_user_id(user_id=user_id, mood=request.mood)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED, tags=["notes"])
def create_note(
	request: CreateNoteRequest,
	user_id: str,
	note_service: NoteService = Depends(get_note_service),
) -> Note:
	"""Create a note for the user provided via query parameter."""
	note = Note(id=uuid4().hex, user_id=user_id, note=request.note)
	return note_service.create(note)


@app.get("/notes/latest", response_model=list[Note], tags=["notes"])
def get_last_five_notes_excluding_user(
	user_id: str,
	note_service: NoteService = Depends(get_note_service),
) -> list[Note]:
	"""Return the latest five notes excluding notes created by the provided user."""
	return note_service.get_last_five_excluding_user(user_id)





