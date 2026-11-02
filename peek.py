import re

def show(file, pattern, width=400, max_hits=3):
    html = open(file, encoding="utf-8").read()
    hits = list(re.finditer(pattern, html, flags=re.I))
    print(f"\n##### {file} | pattern: {pattern} | hits: {len(hits)}")
    for m in hits[:max_hits]:
        s = max(0, m.start() - width)
        e = min(len(html), m.end() + width)
        print("-" * 50)
        print(html[s:e])

show("endgame.html", r"\d{1,2}:\d{2}\s?(AM|PM)")
show("doomsday.html", r"showtime")
show("doomsday.html", r"coming soon")