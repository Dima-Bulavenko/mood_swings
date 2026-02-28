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



# Mood Swings Data Analytics Documentation

## Overview
This module implements a comprehensive data analytics and machine learning pipeline for the Mood Swings project, handling synthetic mood data from 700 records (50 users × 14 days) stored in SQLite database and CSV format.

## Database Overview
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

## Key Features
**Data Pipeline**: Follows a structured 7-step process including data generation, EDA, feature engineering, model training, evaluation, saving, and wordcloud generation.
**Data Seeding**: Load initial data from CSV file into the database using pandas. The CSV serves as the data source for analysis, while the database provides persistent storage for application runtime access.
**Models**: Implements Random Forest and XGBoost classifiers to predict user town based on mood, hour of day, and day of week features. Both achieve 100% accuracy on synthetic data.
**Feature Engineering**: Converts categorical mood labels to numerical values, applies MinMaxScaler normalization, and splits data 80/20 for training/testing.
**Visualizations**: Includes EDA charts (bar charts, heatmaps, Plotly interactive visualizations) and town-specific wordclouds generated from user notes with custom color themes.

## Output Artifacts
- Training data: `data/mood_swing_data.csv`
- Trained model: `mood_model.joblib`
- Wordclouds: `assets/wordclouds/{calm-down_corner, happy_place, up-sad_down}.png`

## Tech Stack
Python (Pandas, Scikit-learn, XGBoost, Plotly, WordCloud)

## Future Enhancements
Real user data migration, sentiment analysis, time-series modeling, API productionization.