import json
import re
import sys

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
DECODER = json.JSONDecoder()

DEFAULT_URL = "https://goldeneaglecinemasgh.com/movies/1003596-avengers-doomsday"


import time

def fetch_html(url: str, retries: int = 4) -> str:
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(
                url,
                headers=HEADERS,
                timeout=(10, 60),  # (connect, read) seconds
            )
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException as e:
            last_err = e
            wait = attempt * 5
            print(f"Attempt {attempt}/{retries} failed: {type(e).__name__}. Retrying in {wait}s...")
            time.sleep(wait)
    raise last_err


def flight_text(html: str) -> str:
    """Rebuild the JSON data Next.js streams inside <script> tags."""
    chunks = re.findall(
        r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, flags=re.S
    )
    parts = []
    for c in chunks:
        try:
            parts.append(json.loads('"' + c + '"'))
        except json.JSONDecodeError:
            parts.append(c.replace('\\"', '"'))
    return "".join(parts)


def get_showtimes(url: str = DEFAULT_URL) -> dict:
    """Returns {date: [times]}. Empty dict means no showtimes published."""
    text = flight_text(fetch_html(url))
    key = '"showtimesByDate":'
    i = text.find(key)
    if i == -1:
        raise ValueError("showtimesByDate not found - site layout may have changed")

    data, _ = DECODER.raw_decode(text, i + len(key))

    result = {}
    for entry in data:
        times = entry.get("times")
        if isinstance(times, list):
            if times:
                result[entry["date"]] = times
        elif times:  # a reference string instead of a list
            result[entry["date"]] = ["(see website for time)"]
    return result


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    shows = get_showtimes(url)
    if not shows:
        print("No showtimes published yet.")
    else:
        for date, times in shows.items():
            print(date, "->", ", ".join(times))