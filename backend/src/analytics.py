import pandas as pd
from collections import Counter

def load_data(path="mood_swing_data.csv"):
    df = pd.read_csv(path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_of_week'] = df['timestamp'].dt.day_name()
    return df


def mood_frequency(df):
    """
    Returns a dict of mood counts across all users
    """
    return df['mood'].value_counts().to_dict()


def weekly_mood_trend(df):
    """
    Returns a dict: for each day of the week, counts of each mood
    """
    weekly = df.groupby(['day_of_week', 'mood']).size().reset_index(name='count')
    pivot = weekly.pivot(index='day_of_week', columns='mood', values='count').fillna(0)

    days_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    pivot = pivot.reindex(days_order)

    return pivot.to_dict()


def top_happy_words(df, n=10):
    """
    Returns the top n most common meaningful words in happiness notes.
    Filters out common English stopwords.
    """
    # Basic stopwords list (you can expand if needed)
    stopwords = {"a","an","the","with","my","and","of","for","to","in","on","at","is","it","was","had","this","that"}
    
    happy_notes = df[df['mood']=="happy"]['note'].dropna()
    text = " ".join(happy_notes).lower()
    words = text.split()
    
    # Remove stopwords
    meaningful_words = [w for w in words if w not in stopwords]
    
    return Counter(meaningful_words).most_common(n)


def user_mood_history(df, user_id):
    """
    Returns a list of dicts representing a single user's mood history over time
    Each dict: {'timestamp': ..., 'mood': ...}
    """
    user_df = df[df['user_id'] == user_id].sort_values('timestamp')
    return user_df[['timestamp','mood']].to_dict(orient='records')