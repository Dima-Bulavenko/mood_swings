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
This project features a FastAPI backend with analytics engine. 
-  **Daily mood selection** - users can log their mood once per day
-  **Mood towns** - explore different towns based on your mood
  - The Happy Place - share and read notes about what made users happy
  - The UP-SAD Down - tips to help cope with sadness
  - The Calm-Down Corner - breathing exercises to help calm down
-  **Word cloud** - live word cloud showing current moods of all users
-  **Mood dashboard** - view mood trends and data insights including:
  - Most common moods among users
  - Most popular mood by day of the week
  - Personal mood history over the last 7 days
  - Most common words from happiness notes
- **Data Pipeline**: Follows a structured 7-step process including:
	- Data generation
	- EDA
	- Feature engineering
	- Model training
	- Evaluation
	- Saving
	- Wordcloud generation.
- **Data Seeding**: Load initial data from CSV file into the database using pandas.
	- The CSV serves as the data source for analysis, while the database provides persistent storage for application runtime access.
- **Models**: Implements Random Forest and XGBoost classifiers to predict:
	- User town based on mood
	- hour of day, and day of week features
	- Both achieve 100% accuracy on synthetic data.
- **Feature Engineering**
	- Converts categorical mood labels to numerical values
	- Applies MinMaxScaler normalization 
	- Splits data 80/20 for training/testing.
- **Visualizations**: Includes EDA charts
	- Bar charts
	- Heatmaps
	- Plotly interactive visualizationsa
	- Town-specific wordclouds
- **Custom 404 page**
- **User Sessions** – Anonymous session creation using UUIDs, managed via browser local storage
- **Mood Tracking** – Log 1–3 moods per day from the full set of supported mood types (see the backend `MoodType` enum / API docs)
- **Happiness Notes** – Submit notes (≤100 characters) and read others' recent notes
- **Analytics Dashboard** – API endpoints exposing mood frequency, weekly trends, top words/word frequency, and personal history

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
 ---
 ## Future Enhancements
- Sentiment analysis
- Time-series modeling
- API productionization.
- JWT/OAuth authentication
- Docker deployment
- PostgreSQL
- Unit tests
- Rate limiting

## Credits & Acknowledgements
This project was built by the Mood Coders team:
- [Monica] — Frontend
- [Dario] — Frontend
- [Dima] — Backend
- [Victor] — Backend
- [Femi] — Data
- [Chahinez] — Data

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