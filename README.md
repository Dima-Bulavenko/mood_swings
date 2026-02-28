# Setup with `uv`

If you have never used `uv` before, follow these steps.

## 1) Install `uv`

Install using the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Check installation:

```bash
uv --version
```

## 2) Install project dependencies with `uv`

This project backend uses `pyproject.toml` in `backend/`.

```bash
cd backend
uv sync
```

`uv sync` creates a local virtual environment and installs all dependencies from `pyproject.toml`.

## 3) Activate `.venv`

After `uv sync`, activate the virtual environment:

Linux/macOS (bash/zsh):

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

## 4) Run FastAPI server

From `backend/` (with `.venv` activated), start the dev server:

```bash
uv run fastapi dev
```

Then open: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

## 5) Seed the database with sample data

`backend/seed_data.py` populates the database with realistic sample data useful for development and data analytics:

- **100 users** with five personality profiles (optimist, pessimist, anxious, balanced, calm)
- **~8 000 mood entries** spread across the last 90 days — users occasionally skip days, and weekends skew slightly happier
- **~1 600 happiness notes** (≤ 100 chars each) written on days when the user logged a positive mood

Run it from the `backend/` directory (no extra dependencies needed beyond the project's own):

```bash
cd backend
uv run python seed_data.py
```

The script is **idempotent per run** — each execution generates fresh UUIDs, so running it a second time adds another batch of 100 users. To start fresh, delete `mood_swings.db` before re-running.

## Team Git Flow (Simple)

### Roles
- **Developer**: works in a feature branch, opens PR, fixes requested changes.
- **Reviewer**: reviews PR and approves (at least 1 teammate).

### Step-by-step
1. **Sync base branch**
	```bash
	git checkout main
	git pull origin main
	```

2. **Create feature branch** (never code on `main`)
	```bash
	git checkout -b feature/header-fix
	```

3. **Code + commit often** (small save points)
	```bash
	git add .
	git commit -m "feat: fix header layout"
	```

4. **Daily sync with `main`** (avoid big conflicts)
	```bash
	git checkout main
	git pull origin main
	git checkout feature/header-fix
	git merge main
	```

5. **Push and open PR**
	```bash
	git push -u origin feature/header-fix
	```
	Then open a Pull Request to `main`.

6. **Review and refine**
	- Reviewer leaves comments.
	- Developer commits fixes to the same feature branch.

7. **Merge and delete branch**
	- After approval, merge PR into `main`.
	- Delete the feature branch (remote + local).

### If two people edit the same file
- **First merged branch wins**: their code is already in `main`.
- **Second branch gets a merge conflict** during sync/merge with `main`.
- **Fix**: open the conflicted file, choose the correct lines (or combine both), save, then complete merge and commit.

**Rule**: the person who gets the conflict resolves it. If unclear, do a quick call with the teammate who changed the other version.
---

# Mood Swings

## About
Mood Swings is a web app that allows users to track and explore their daily moods. 
Users can select their mood each day and visit different "towns" based on how they 
are feeling. Each town offers a unique experience, from sharing happy notes to 
breathing exercises. Each page also displays a live word cloud showing the current 
moods of all users. Users can also view mood trends on the dashboard.

## Live Link

## Deployment


## Wireframes
- Wireframes created using AI image generation

![App Flow](/frontend/assets/images/wireframe1.png)
![Town Map](/frontend/assets/images/wireframe2.png)

## Features
- 🎭 **Daily mood selection** - users can log their mood once per day
- 🏘️ **Mood towns** - explore different towns based on your mood
  - The Happy Place - share and read notes about what made users happy
  - The UP-SAD Down - tips to help cope with sadness
  - The Calm-Down Corner - breathing exercises to help calm down
- ☁️ **Word cloud** - live word cloud showing current moods of all users
- 📊 **Mood dashboard** - view mood trends and data insights including:
  - Most common moods among users
  - Most popular mood by day of the week
  - Personal mood history over the last 7 days
  - Most common words from happiness notes
- **Data Pipeline**: Follows a structured 7-step process including data generation, EDA, feature engineering, model training, evaluation, saving, and wordcloud generation.
- **Data Seeding**: Load initial data from CSV file into the database using pandas. The CSV serves as the data source for analysis, while the database provides persistent storage for application runtime access.
- **Models**: Implements Random Forest and XGBoost classifiers to predict user town based on mood, hour of day, and day of week features. Both achieve 100% accuracy on synthetic data.
- **Feature Engineering**: Converts categorical mood labels to numerical values, applies MinMaxScaler normalization, and splits data 80/20 for training/testing.
- **Visualizations**: Includes EDA charts (bar charts, heatmaps, Plotly interactive visualizations) and town-specific wordclouds generated from user notes with custom color themes.
- 🚫 Custom 404 page — a styled page is in place for any unknown routes, 
wired up and served by the backend when a user navigates to a page that doesn't exist

## ScreenShots
![Home Page](/frontend/assets/images/Screenshot-index.png)
![Mood Tracker](/frontend/assets/images/Screenshot-moodtracker.png)
![Up-SAD Down](/frontend/assets/images/Screenshot-UPSADdown.png)

## Frontend
 ### Technologies Used
- HTML5 
- CSS3 
- JavaScript (ES6)
- Bootstrap 5

### Folder Structure
```
frontend/
├── assets/
│   ├── css/
│   │   ├── calm-town.css
│   │   ├── dashboard.css
│   │   ├── index.css
│   │   ├── happinesstown.css
│   │   └── sadness-town.css
│   ├── js/
│   │   ├── calm-town.js
│   │   ├── dashboard.js
│   │   ├── index.js
│   │   ├── happinesstown.js
│   │   ├── sadness-town.js
│   │   └── client.js
│   └── images/
├── calm-town.html
├── dashboard.html
├── index.html
├── happinesstown.html
├── sadness-town.html
└── 404.html
```

### How to Run Locally
1. Clone the repository
2. Open the `frontend` folder
3. Open `index.html` in your browser

> 💡 We recommend using the **Live Server** extension in VS Code for the best experience

## Backend

This project features a FastAPI backend with analytics engine. Users log daily moods, write happiness notes, and explore emotional trends through interactive charts.

### Features

- **User Sessions** – Anonymous session creation using UUIDs, managed via browser local storage
- **Mood Tracking** – Log 1–3 moods per day from the full set of supported mood types (see the backend `MoodType` enum / API docs)
- **Happiness Notes** – Submit notes (≤100 characters) and read others' recent notes
- **Analytics Dashboard** – API endpoints exposing mood frequency, weekly trends, top words/word frequency, and personal history

### Architecture

The backend follows a layered architecture:

- **Domain** – Core business models and DTOs
- **Infrastructure** – SQLAlchemy ORM and repositories
- **Service** – Business logic and analytics
- **API** – FastAPI routes

### Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- `uv` (dependency manager)

### Project Structure

```
backend/
├── core/domain/
├── infrastructure/sqlalchemy/
├── service/
├── main.py
├── seed_data.py
├── pyproject.toml
└── mood_swings.db  # generated at runtime
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create anonymous session |
| POST | `/moods?user_id=` | Create today's mood |
| GET | `/moods/today?user_id=` | Retrieve today's mood |
| PUT | `/moods/today?user_id=` | Update today's mood |
| POST | `/notes?user_id=` | Create happiness note |
| GET | `/notes/latest?user_id=` | Get 5 most recent notes from other users |
| GET | `/mood-frequency` | Top 5 moods |
| GET | `/weekly-trend` | Mood by weekday |
| GET | `/top-happy-words` | Top 10 words |
| GET | `/user-history?user_id=` | 7-day mood history |

### Future Enhancements

- JWT/OAuth authentication
- Docker deployment
- PostgreSQL
- Unit tests
- Rate limiting

---
## Data Analytics

### Overview
This module implements a comprehensive data analytics and machine learning pipeline for the Mood Swings project, handling synthetic mood data from 700 records (50 users × 14 days) stored in SQLite database and CSV format.

### Database Overview
- **Database File**: `mood_swings.db` (SQLite)
- **Purpose**: Persistent storage and querying of mood records
- **Data Source**: Mirrors `data/mood_swing_data.csv`

**Table: moods**
| Column      | Type       | Description                                          |
| ----------- | ---------- | ---------------------------------------------------- |
| id          | INTEGER PK | Unique record identifier                             |
| user_id     | INTEGER    | References user account                              |
| mood        | TEXT       | Mood classification: `"happy"`, `"sad"`, or `"calm"` |
| tags        | TEXT       | Optional additional labels relating to the mood      |
| town_name   | TEXT       | Geographic location associated with the mood         |
| note        | TEXT       | Optional user comments                               |
| hour_of_day | INTEGER    | Hour of the day (0–23)                               |
| day_of_week | INTEGER    | Day of the week (0 = Sunday, 6 = Saturday)           |
| timestamp   | DATETIME   | Recording date and time                              |


### Installation & Setup
Install dependencies and initialize the database with the following steps:
1. Install required packages
2. Import SQLAlchemy base models
3. Create database engine connection
4. Generate all tables from model definitions

### Output Artifacts
- Training data: `data/mood_swing_data.csv`
- Trained model: `mood_model.joblib`
- Wordclouds: `assets/wordclouds/{calm-down_corner, happy_place, up-sad_down}.png`

### Tech Stack
Python (Pandas, Scikit-learn, XGBoost, Plotly, WordCloud)

### Future Enhancements
Real user data migration, sentiment analysis, time-series modeling, API productionization.

## Credits & Acknowledgements

### Images
- The HappyPlace background
https://www.istockphoto.com/vector/abstract-fresh-green-light-yellow-gradient-with-wavy-texture-glowing-smooth-fluid-gm2160692092-581206282
- Calm-Down corner Background
https://www.istockphoto.com/vector/blue-gradient-background-a-seamless-abstract-background-featuring-a-smooth-gradient-gm2197713783-615653745
- The UP-SAD Down Background
https://www.istockphoto.com/vector/calm-pastel-blue-and-violet-mesh-gradient-gm2170087661-590032872
 - Home Page / Dashboard / 404 Background
 https://www.istockphoto.com/vector/abstract-background-gradient-soft-tone-purple-pink-beige-pastel-colors-copy-space-gm2208849925-625984584


### Resources & Links
- [Bootstrap 5](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- You Tube
- Spotify