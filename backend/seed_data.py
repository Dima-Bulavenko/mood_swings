"""
Seed script: populates mood_swings.db with ~100 users, historical moods and happiness notes.

Run from the backend/ directory:
    python seed_data.py

The script is idempotent – running it twice will skip users that already exist.
"""

import random
import sys
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Ensure the backend package is importable when running from the backend/ dir
sys.path.insert(0, str(Path(__file__).parent))

from infrastructure.sqlalchemy.models import Base, MoodModel, NoteModel, UserModel

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./mood_swings.db"
NUM_USERS = 100
DAYS_BACK = 90          # how many days of history to generate
MOOD_SKIP_CHANCE = 0.25  # probability that a user skips a given day entirely

random.seed(42)  # reproducible data

# ---------------------------------------------------------------------------
# Mood pools – grouped by emotional "flavour" for realistic user profiles
# ---------------------------------------------------------------------------
HAPPY_MOODS = ["joyful", "grateful", "excited", "proud", "peaceful", "happy"]
CALM_MOODS = ["peaceful", "meh", "tired"]
SAD_MOODS = ["sad", "lonely", "meh", "hurt", "broken-hearted", "unmotivated", "dejected"]
ANXIOUS_MOODS = ["tired", "angry", "anxious", "overwhelmed", "lost", "spiralling"]
ALL_MOODS = HAPPY_MOODS + SAD_MOODS + ANXIOUS_MOODS

# User "personality" profiles: (name, primary_pool, secondary_pool, primary_weight)
PROFILES = [
    ("optimist",  HAPPY_MOODS,   SAD_MOODS,    0.80),
    ("pessimist", SAD_MOODS,     HAPPY_MOODS,  0.75),
    ("anxious",   ANXIOUS_MOODS, HAPPY_MOODS,  0.70),
    ("balanced",  ALL_MOODS,     ALL_MOODS,    0.50),
    ("calm",      CALM_MOODS,    ANXIOUS_MOODS, 0.65),
]

# ---------------------------------------------------------------------------
# Happiness notes – varied short notes (≤100 chars) for analytics richness
# ---------------------------------------------------------------------------
HAPPY_NOTES = [
    "Had a great coffee with a friend this morning.",
    "Finally finished a project I've been working on for weeks!",
    "My dog greeted me with so much energy – made my day.",
    "Cooked a new recipe and it turned out amazing.",
    "Got a compliment from my colleague today.",
    "Went for a long walk and enjoyed the fresh air.",
    "Read a really inspiring book chapter.",
    "My favourite song came on the radio – instant mood boost.",
    "Received a heartfelt message from an old friend.",
    "Managed to wake up early and watch the sunrise.",
    "Had a really productive day at work.",
    "Tried a new café and loved it.",
    "Helped a stranger with directions and they were so grateful.",
    "Got a surprise gift from my partner.",
    "Finished a workout and felt energized all day.",
    "Watched a funny movie and laughed a lot.",
    "Planted some flowers in the garden.",
    "My team won the game tonight!",
    "Finally solved a bug I had been chasing all week.",
    "Had a peaceful evening reading by the window.",
    "Spent quality time with my family.",
    "Tried meditation for the first time – loved it.",
    "Got promoted at work!",
    "Enjoyed a sunny walk in the park.",
    "Baked cookies and shared them with neighbours.",
    "Had a perfect nap in the afternoon.",
    "Saw a beautiful rainbow on my way home.",
    "Reconnected with a childhood friend.",
    "Finished reading a novel I started months ago.",
    "Had a long, honest conversation with a friend.",
    "My plants are blooming – feels like a win.",
    "Completed my to-do list for the first time this month.",
    "Volunteered at a local shelter and felt fulfilled.",
    "Got great feedback on my presentation.",
    "Enjoyed a quiet evening with good music.",
    "Found a great deal on something I needed.",
    "Had the best homemade meal in a while.",
    "Took a spontaneous road trip and it was wonderful.",
    "Learned a new skill online today.",
    "The weather was perfect – made everything better.",
    "Had a great deep-sleep night.",
    "Finished a difficult workout I nearly gave up on.",
    "Received a heartfelt thank-you from a colleague.",
    "Caught up on a favourite TV show.",
    "Got a message from family that made me smile.",
    "Helped a friend move and it felt good to contribute.",
    "Discovered a new podcast I really enjoy.",
    "Had a peaceful solo lunch in the park.",
    "Made someone laugh today – that always makes me happy.",
    "Finished a creative project I'm really proud of.",
    "Went to a concert and it was incredible.",
    "Cooked a healthy meal and felt great after.",
    "Spent the evening stargazing.",
    "Had a board game night with friends.",
    "Surprised my mum with a call – she was so happy.",
    "Found a beautiful hiking trail near my city.",
    "My favourite sports team scored a big win.",
    "Had an impromptu dance session in the kitchen.",
    "Wrote in my journal and felt lighter afterwards.",
    "Bought myself flowers – small joys matter.",
    "Had a meaningful conversation about life goals.",
    "Fixed something around the house I had been ignoring.",
    "Saw cute puppies at the park today.",
    "Got an unexpected day off – rested well.",
    "Started a new creative hobby.",
    "Had the most delicious meal at a restaurant.",
    "Went swimming and felt refreshed.",
    "Finished a tough exam – huge relief.",
    "My artwork got a lot of positive comments online.",
    "Had a spontaneous dance night with friends.",
    "Received flowers from a loved one.",
    "The sunset today was absolutely stunning.",
    "Felt grateful for my health today.",
    "Had a really fun team-building event at work.",
    "Spent the afternoon playing board games.",
    "Read poetry and felt inspired.",
    "Had the kindest interaction with a stranger.",
    "My vegetable garden produced its first harvest!",
    "Organized my workspace and it feels amazing.",
    "Had a heartfelt reunion with relatives.",
    "Found an old photo album – lovely memories.",
    "Did yoga in the morning – felt calm all day.",
    "Got into a great book I couldn't put down.",
    "Had the most cosy evening by the fireplace.",
    "My best friend surprised me with a visit.",
    "Achieved a personal fitness milestone.",
    "Had a meaningful moment volunteering today.",
    "Everything just clicked today – great flow.",
    "Adopted a rescue cat – so happy!",
    "Had a spontaneous picnic with family.",
    "Learned something fascinating about the universe.",
    "Got a handwritten letter – rare and touching.",
    "Donated to a cause I care about.",
    "Spent quality time with my kids today.",
    "Made a new friend at an event.",
    "Finished decorating my room – love it.",
    "Had a refreshing swim in the sea.",
    "Cooked breakfast in bed for my partner.",
    "Saw a shooting star on a night walk.",
]

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def build_session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()


def pick_moods_for_day(profile, day_of_week: int) -> list[str]:
    """Return 1-3 mood strings for a single day, influenced by profile & weekday."""
    _, primary, secondary, weight = profile

    # Weekends skew slightly happier for everyone
    if day_of_week in (5, 6):
        weight = min(weight + 0.10, 1.0) if primary == HAPPY_MOODS else weight

    pool = primary if random.random() < weight else secondary
    mood = random.choice(pool)

    # 20% chance of a second mood
    moods = [mood]
    if random.random() < 0.20:
        moods.append(random.choice(pool))

    return list(set(moods))  # deduplicate


def is_happy_mood(mood: str) -> bool:
    return mood in HAPPY_MOODS


def main():
    session = build_session()

    # Fetch existing user ids to avoid duplicates
    existing_ids = {row[0] for row in session.execute(text("SELECT id FROM users")).fetchall()}
    print(f"Existing users in DB: {len(existing_ids)}")

    today = date.today()
    users_created = 0
    moods_created = 0
    notes_created = 0

    for i in range(NUM_USERS):
        user_id = uuid4().hex

        # Skip if somehow already present (shouldn't happen with fresh UUIDs)
        if user_id in existing_ids:
            continue

        profile = PROFILES[i % len(PROFILES)]

        # Insert user
        session.add(UserModel(id=user_id))
        users_created += 1

        # Generate mood + optional note for each day in the history window
        available_notes = HAPPY_NOTES.copy()
        random.shuffle(available_notes)
        note_index = 0

        for days_ago in range(DAYS_BACK, -1, -1):  # oldest → newest
            if random.random() < MOOD_SKIP_CHANCE:
                continue  # user skipped this day

            entry_date = today - timedelta(days=days_ago)
            day_of_week = entry_date.weekday()

            moods = pick_moods_for_day(profile, day_of_week)
            has_happy = any(is_happy_mood(m) for m in moods)

            for mood_str in moods:
                session.add(MoodModel(
                    id=uuid4().hex,
                    user_id=user_id,
                    mood=mood_str,
                    date_create=entry_date,
                ))
                moods_created += 1

            # Leave a happiness note ~60% of the time on happy days
            if has_happy and random.random() < 0.60:
                note_text = available_notes[note_index % len(available_notes)]
                note_index += 1
                session.add(NoteModel(
                    id=uuid4().hex,
                    user_id=user_id,
                    note=note_text,
                    date_create=entry_date,
                ))
                notes_created += 1

    session.commit()
    session.close()

    print(f"✅  Seed complete:")
    print(f"   Users created  : {users_created}")
    print(f"   Moods created  : {moods_created}")
    print(f"   Notes created  : {notes_created}")


if __name__ == "__main__":
    main()
