# Mood Swings — Project Description

## 💡 Project Overview

**Mood Swings** is a web application where users:

- Select their daily mood
- Enter a town based on that mood
- Interact with simple emotional features
- View their personal mood analytics on a separate dashboard

The **towns** focus on emotional experience.
The **dashboard** focuses on data insights.

---

## 🏙 The Three Towns

### 🌞 Happiness Town

**Purpose:** Spread positivity.

**Features:**

- User answers: **“What made you happy today?”**
- The note is saved in the database
- Notes appear on a public positivity board
- Users can read messages from others

### 🌸 Calm Town

**Purpose:** Help users relax.

**Features:**

- Simple breathing animation
  - or -
- Soft relaxing background music

### 🌧 Sadness Town

**Purpose:** Provide emotional support.

**Features:**

- Display encouraging supportive message
  - or -
- Generate short AI-based supportive message

**Example:**

> “It’s okay to have difficult days. Tomorrow is a new start.”

---

## 📊 Mood Insights Dashboard

This is a separate page where all analytics charts are shown.

### 1) Mood Frequency

- Count how many times each mood was selected
- Display as a bar chart


### 2) Weekly Mood Pattern

- Analyze mood by day of the week
- Display as line chart or grouped bar chart


### 3) Happiness Word Analysis

- Analyze text from Happiness Town notes
- Count most common meaningful words
- Display top 10 words as a bar chart

**Example insight:**

> “Friends” and “family” are your most common happiness sources.

---

## ⚙ Technical Stack

### Frontend

- HTML
- CSS
- Bootstrap
- Vanilla JavaScript
- Chart.js (for charts)

### Backend

- FastAPI
- SQLite
- Pandas (for analysis)

---

## 🗄 Database Structure

### `users`

- `id` (UUID)

### `moods`

- `id`
- `user_id`
- `mood` (`happy`, `calm`, `sad`)
- `note` (for happiness entries)
- `date`

---

## 🎯 User Flow

1. User enters the site.
2. Session UUID is created and stored.
3. User selects mood.
4. User visits a town.
5. Data is saved.
6. User opens the Mood Insights dashboard to see charts and insights.
