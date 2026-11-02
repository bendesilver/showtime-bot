import re
import requests
from bs4 import BeautifulSoup

URLS = {
    "endgame (has showtimes)": "https://goldeneaglecinemasgh.com/movies/299534-avengers-endgame",
    "doomsday (coming soon)": "https://goldeneaglecinemasgh.com/movies/1003596-avengers-doomsday",
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for label, url in URLS.items():
    print("=" * 60)
    print(label)
    r = requests.get(url, headers=HEADERS, timeout=20)
    print("Status:", r.status_code, "| Length:", len(r.text))
    fname = "endgame.html" if "endgame" in label else "doomsday.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(r.text)

    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text(" ", strip=True)
    print("Mentions 'showtime':", "showtime" in text.lower())
    print("Mentions 'coming soon':", "coming soon" in text.lower())
    print("Time-like strings (e.g. 7:30):", re.findall(r"\b\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?", text)[:10])
    print("Script tags:", len(soup.find_all("script")))
    print("Has __NEXT_DATA__:", "__NEXT_DATA__" in r.text)
    print("API-like URLs:", sorted(set(re.findall(r'https?://[^"\']*api[^"\']*', r.text)))[:10])