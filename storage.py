import json
import os

STATE_FILE = os.path.join("data", "state.json")


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except json.JSONDecodeError:
        return {}


def save_state(state: dict):
    os.makedirs("data", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def find_new(old, new: dict) -> dict:
    old = old or {}
    added = {}
    for date, times in new.items():
        fresh = [t for t in times if t not in old.get(date, [])]
        if fresh:
            added[date] = fresh
    return added