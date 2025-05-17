import pandas as pd
from collections import Counter
from itertools import combinations
import re

def load_data(path):
    df = pd.read_csv("D:/Social/tweets.csv")
    # Explicitly convert 'date_time' to datetime type
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    
    # Normalize text content to lowercase string
    df['content'] = df['content'].astype(str).str.lower()
    return df

def get_available_filters(df):
    return {
        'countries': sorted(df['country'].dropna().unique().tolist()),
        'languages': sorted(df['language'].dropna().unique().tolist())
    }

def filter_df_by_country_language(df, country=None, language=None):
    filtered = df
    if country:
        filtered = filtered[filtered['country'] == country]
    if language:
        filtered = filtered[filtered['language'] == language]
    return filtered

def extract_words(text):
    # Extract words ignoring special characters and digits, only words with at least 2 letters
    return re.findall(r'\b[a-z]{2,}\b', text)

def get_top_words_trends(df, top_n=5):
    # Remove rows with invalid date_time
    df = df.dropna(subset=['date_time'])
    
    # Group by date only (drop time)
    df['date_only'] = df['date_time'].dt.date
    date_groups = df.groupby('date_only')['content'].apply(lambda texts: ' '.join(texts))
    
    all_counts = []
    dates = []
    for date, texts in date_groups.items():
        words = extract_words(texts)
        counter = Counter(words)
        most_common = counter.most_common(top_n)
        all_counts.append({w:c for w,c in most_common})
        dates.append(date)
    
    # Unique top words across all dates
    top_words = list({w for d in all_counts for w in d.keys()})
    
    # Create dataframe with counts for each top word per date
    data = pd.DataFrame(all_counts, index=dates).fillna(0).astype(int)
    return data, top_words

def get_top_cooccurrences(df, top_n=10):
    pairs_counter = Counter()
    for text in df['content']:
        words = set(extract_words(text))
        for pair in combinations(sorted(words), 2):
            pairs_counter[pair] += 1
    return pairs_counter.most_common(top_n)

def get_top_likes_shares(df, top_n=10):
    word_engagement = Counter()
    for _, row in df.iterrows():
        words = extract_words(row['content'])
        engagement = row.get('number_of_likes', 0) + row.get('number_of_shares', 0)
        for w in set(words):
            word_engagement[w] += engagement
    top_words = word_engagement.most_common(top_n)
    return [{'word': w, 'engagement': e} for w, e in top_words]

def get_countrywise_counts(df):
    counts = df['country'].value_counts().to_dict()
    return [{'country': k, 'count': v} for k, v in counts.items()]
