from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.domain.mood import Mood, MoodType
from core.domain.analytics import MoodFrequencyChart, TopHappyWordsChart, UserMoodHistoryChart, WeeklyPopularMoodChart
from core.domain.note import Note
from core.domain.user import User
from infrastructure.sqlalchemy.models import Base
from infrastructure.sqlalchemy.repositories.mood_repository import SQLAlchemyMoodRepository
from infrastructure.sqlalchemy.repositories.note_repository import SQLAlchemyNoteRepository
from infrastructure.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository
from service.analytics_service import AnalyticsService
from service.mood_service import MoodService
from service.note_service import NoteService
from service.user_service import UserService

from environs import env

env.read_env(override=True)
DEBUG = env.bool("DEBUG", default=True)

DATABASE_URL = "sqlite:///./mood_swings.db"

if DEBUG is False:
    DATABASE_URL = env.str("DATABASE_URL", default=DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateMoodRequest(BaseModel):
    moods: list[MoodType] = Field(min_length=1)


class UpdateMoodRequest(BaseModel):
    moods: list[MoodType] = Field(min_length=1)


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


def get_analytics_service(session: Session = Depends(get_session)) -> AnalyticsService:
    mood_repository = SQLAlchemyMoodRepository(session)
    note_repository = SQLAlchemyNoteRepository(session)
    return AnalyticsService(mood_repository, note_repository)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user_service: UserService = Depends(get_user_service)) -> User:
    """Create a new user and return the generated user identifier."""
    return user_service.create_user()


@app.post("/moods", response_model=list[Mood], status_code=status.HTTP_201_CREATED, tags=["moods"])
def create_mood(
    request: CreateMoodRequest,
    user_id: str,
    mood_service: MoodService = Depends(get_mood_service),
) -> list[Mood]:
    """Create multiple today's mood entries for the user provided via query parameter."""
    return mood_service.create_moods(user_id=user_id, moods=request.moods)


@app.get(
    "/moods/today",
    response_model=list[Mood],
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
) -> list[Mood]:
    """Retrieve all today's moods for the user provided via query parameter."""
    try:
        return mood_service.get_todays_moods_by_user_id(user_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.put(
    "/moods/today",
    response_model=list[Mood],
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
) -> list[Mood]:
    """Replace today's mood choices for the user provided via query parameter."""
    try:
        return mood_service.update_todays_moods_by_user_id(user_id=user_id, moods=request.moods)
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


@app.get("/mood-frequency", response_model=MoodFrequencyChart, tags=["analytics"])
def get_mood_frequency_endpoint(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> MoodFrequencyChart:
    """Return top 5 most common moods"""
    return analytics_service.get_top_mood_frequency_chart(limit=5)


@app.get("/weekly-trend", response_model=WeeklyPopularMoodChart, tags=["analytics"])
def get_weekly_trend_endpoint(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> WeeklyPopularMoodChart:
    """Return the most popular mood for each day of the week."""
    return analytics_service.get_weekly_popular_mood_chart()


@app.get("/top-happy-words", response_model=TopHappyWordsChart, tags=["analytics"])
def get_top_happy_words_endpoint(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> TopHappyWordsChart:
    """Return top 10 most common words in users' happiness notes."""
    return analytics_service.get_top_happy_words_chart(limit=10)


@app.get("/user-history", response_model=UserMoodHistoryChart, tags=["analytics"])
def get_user_history_endpoint(
    user_id: str,
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> UserMoodHistoryChart:
    """Return user mood history for the last 7 days with missing days as null."""
    return analytics_service.get_user_mood_history_chart(user_id=user_id, days=7)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Health check endpoint to verify that the service is running."""
    return {"status": "ok"}


handler = Mangum(app, lifespan="off")
