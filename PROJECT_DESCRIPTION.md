# Mood Swings — Project Description

## Pages
The project consists of the following pages:
- Home (index.html)
- Town's pages, one for each town. I suggest to have only 3 towns (Happiness, Sadness, and Calmness) but in the future we can add more.
The names of the pages can be changed to more creative ones.
- Data Analysis


## Project Flow by pages

### Home Page
#### Flow:
1. User navigates to the page for the first time.
2. Frontend checks user's local storage for user's token.
    - 2.1 if tnehe token is not found, frontend make a request to the backend to create a w token and create a new user session. The token is returned to the frontend and stored in the local storage.
    - 2.2 if the token is found, frontend makes uses this token in upcoming requests to the backend.
3. User is suggested to choose their mood today (exited, happy, calm, sad, angry). User is able to choose one mood per day. If user choose one the they should be able to see a button to change their day's mood. If user skip mood selection, they should be able to see a button to choose their day's mood.
4. On the main page, user can see the towns with short description of them, and can navigate to each town to explore their features.

### The Happy Place (happiness-town.html)
#### Features:
1. Read other users' notes about what made them happy today.
2. Leave their own note about what made them happy today.
related words: Happy, Peaceful, Proud, Excited, Grateful, Joyful

### The UP-SAD Down (sadness-town.html)
#### Features:
1. Show some tips that can help users to cope with sadness.
related words: Sad, Lonely, Meh, Hurt, Broken-Hearted, Unmotivated, Dejected

### The Calm-Down Corner (calm-town.html)
#### Features:
1. Breathing exercises to help users to calm down.
related words: Spiralling, Lost, overwhelmed, Anxious, Angry, Tired

### Mood Tracker (dashboard.html)
#### Features:
To create a chart we can use a library Chart.js.
1. Show a bar chart of the most common moods among users.
2. Show a chart of what is the most popular mood for each day of the week.
3. Show a history of the user's moods over time.
4. Show the most common words in users' happiness notes.


## Some notes:
- Check what is the fetch in JS and how to use axios (this is more modern implementation of fetch). This technologies help to do requests to the backend and get data from it.
