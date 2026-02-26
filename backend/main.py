from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.analytics import load_data, mood_frequency, weekly_mood_trend, top_happy_words, user_mood_history


app = FastAPI(title="Mood Swings Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = load_data("../data/mood_swing_data.csv")  


@app.get("/mood-frequency")
def get_mood_frequency_endpoint():
    return mood_frequency(df)

@app.get("/weekly-trend")
def get_weekly_trend_endpoint():
    return weekly_mood_trend(df)

@app.get("/top-happy-words")
def get_top_happy_words_endpoint():
    return top_happy_words(df)

@app.get("/user-history/{user_id}")
def get_user_history_endpoint(user_id: str):
    return user_mood_history(df, user_id)