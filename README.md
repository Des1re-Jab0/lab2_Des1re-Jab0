# Lab 2: The Social Media Data Detective

## Files
- `data-detective.py` — cleans, analyzes, sorts, and searches the tweet dataset
- `feed-analyzer.sh` — shell one-liner pipeline that prints the Top 5 most active users
- `twitter_dataset.csv` — the dataset used for testing (from Kaggle)

## How to run the Python app

```bash
python3 data-detective.py
```

It will:
1. Load `twitter_dataset.csv` (must be in the same folder)
2. Clean the data and report how many rows were fixed/removed
3. Print the single most viral tweet (highest Likes)
4. Print the Top 10 tweets sorted by Likes (custom sort, no `.sort()`/`sorted()`/`max()`)
5. Prompt you for a keyword and print how many tweets matched, plus the matches

## How to run the shell script

```bash
chmod +x feed-analyzer.sh
./feed-analyzer.sh
```

It prints the Top 5 most active users (by tweet count) directly from `twitter_dataset.csv`,
using a `cut | sort | uniq -c | sort -nr | head -5` pipeline. Because some tweets contain
embedded commas and line breaks inside quoted text, the script first flattens each multi-line
quoted record onto a single line before running that pipeline.

## Sorting algorithm

`custom_sort_by_likes` uses a **Selection Sort**: for each position in the list, it scans the
remaining unsorted items to find the one with the highest `Likes`, then swaps it into place —
repeating until the whole list is ordered from most-liked to least-liked.

