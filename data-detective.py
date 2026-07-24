import csv
import sys
import os
import time


def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    raw_tweets = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                raw_tweets.append(row)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    return raw_tweets


def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    cleaned = []
    skipped = 0

    for tweet in tweets:
        text = (tweet.get('Text') or '').strip()
        if not text:
            skipped += 1
            continue  # a tweet with no text isn't usable data

        likes_raw = (tweet.get('Likes') or '').strip()
        retweets_raw = (tweet.get('Retweets') or '').strip()

        try:
            likes = int(likes_raw) if likes_raw else 0
        except ValueError:
            likes = 0

        try:
            retweets = int(retweets_raw) if retweets_raw else 0
        except ValueError:
            retweets = 0

        cleaned.append({
            'Username': (tweet.get('Username') or 'unknown').strip(),
            'Text': text,
            'Likes': likes,
            'Retweets': retweets
        })

    if skipped:
        print(f"Skipped {skipped} row(s) with missing text.")

    return cleaned


def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    Do not use the max() function.
    """
    if not tweets:
        return None  # empty list has no "most liked" tweet

    best = tweets[0]
    for tweet in tweets[1:]:
        if tweet['Likes'] > best['Likes']:
            best = tweet
    return best


def custom_sort_by_likes(tweets):
    """
    QUEST 3: Implement Bubble Sort or Selection Sort to sort the list
    by 'Likes' in descending order. NO .sort() allowed!
    """
    data = list(tweets)  # don't mutate the caller's list
    n = len(data)

    # Selection sort, descending: for each position, find the largest
    # remaining element and swap it into place. O(n^2) but only does
    # one swap per pass instead of bubble sort's many swaps.
    for i in range(n):
        best_index = i
        for j in range(i + 1, n):
            if data[j]['Likes'] > data[best_index]['Likes']:
                best_index = j
        if best_index != i:
            data[i], data[best_index] = data[best_index], data[i]

    return data


def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    if not keyword:
        return []

    keyword_lower = keyword.lower()
    matches = []
    for tweet in tweets:
        if keyword_lower in tweet['Text'].lower():
            matches.append(tweet)
    return matches


if __name__ == "__main__":
    # Load the messy data
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")

    # Quest 1: clean
    clean_dataset = clean_data(dataset)
    print(f"{len(clean_dataset)} tweets remain after cleaning.\n")

    # Quest 2: find the viral tweet
    viral = find_viral_tweet(clean_dataset)
    if viral:
        print("--- Most Viral Tweet ---")
        print(f"@{viral['Username']} | Likes: {viral['Likes']} | {viral['Text'][:80]}...")
    else:
        print("No tweets to analyze.")
    print()

    # Quest 3: sort by likes, descending (only sorting a sample for speed)
    print("--- Top 10 Tweets by Likes (sorted) ---")
    start = time.time()
    sorted_tweets = custom_sort_by_likes(clean_dataset)
    elapsed = time.time() - start
    for t in sorted_tweets[:10]:
        print(f"@{t['Username']} | Likes: {t['Likes']}")
    print(f"(sort took {elapsed:.2f}s for {len(clean_dataset)} tweets)\n")

    # Quest 4: keyword search
    keyword = input("Enter a keyword to search for: ")
    results = search_tweets(clean_dataset, keyword)
    print(f"--- Tweets containing '{keyword}': {len(results)} found ---")
    for t in results[:3]:
        print(f"@{t['Username']}: {t['Text'][:80]}...")

