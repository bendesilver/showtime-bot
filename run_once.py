import os
from dotenv import load_dotenv

from scraper import get_showtimes
from notifier import send_message
from storage import load_state, save_state, find_new

load_dotenv()
URL = os.getenv("MOVIE_URL")
FAIL_ALERT_AFTER = 6  # consecutive failed checks before warning you


def main():
    state = load_state()
    failures = state.get("failures", 0)

    try:
        shows = get_showtimes(URL)
    except Exception as e:
        failures += 1
        print(f"Check failed ({failures} in a row): {e}")
        if failures == FAIL_ALERT_AFTER:
            send_message(
                f"⚠️ Showtime bot has failed {failures} checks in a row. "
                "The site may be down or its layout may have changed."
            )
        state["failures"] = failures
        save_state(state)
        return

    if failures >= FAIL_ALERT_AFTER:
        send_message("✅ Showtime bot can read the page again.")

    added = find_new(state.get("shows"), shows)
    if added:
        lines = ["🎬 Avengers: Doomsday showtimes are up!", ""]
        for date, times in added.items():
            lines.append(f"{date}: {', '.join(times)}")
        lines += ["", URL]
        if send_message("\n".join(lines)):
            state["shows"] = shows
        else:
            print("Telegram send failed; will retry next run")
    else:
        state["shows"] = shows
        print("No new showtimes")

    state["failures"] = 0
    save_state(state)


if __name__ == "__main__":
    main()