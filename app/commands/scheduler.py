from __future__ import annotations

import os
import time
from datetime import datetime

from dotenv import load_dotenv
import schedule

from app.commands.autoclose_overdue import run_autoclose_overdue


def _run_autoclose_job() -> None:
    """Wrapper job that runs the autoclose command and logs basic info."""
    now = datetime.utcnow().isoformat()
    print(f"[scheduler] Running autoclose_overdue at {now} (UTC)")
    closed_count = run_autoclose_overdue()
    print(f"[scheduler] Closed {closed_count} task(s)")


def run_scheduler() -> None:
    """
    Run a simple in-process scheduler that periodically closes overdue tasks.

    Interval is controlled by AUTOCLOSE_INTERVAL_MINUTES in the environment,
    defaulting to 60 minutes if not set.
    """
    load_dotenv()

    interval_minutes = int(os.getenv("AUTOCLOSE_INTERVAL_MINUTES", "60"))
    if interval_minutes <= 0:
        raise ValueError("AUTOCLOSE_INTERVAL_MINUTES must be a positive integer.")

    # Schedule the job to run periodically
    schedule.every(interval_minutes).minutes.do(_run_autoclose_job)

    print(
        f"[scheduler] Started. "
        f"Interval: every {interval_minutes} minute(s). Press Ctrl+C to stop."
    )

    # Optional: run once at startup
    _run_autoclose_job()

    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("[scheduler] Stopped by user.")
    except Exception as exc:
        print(f"[scheduler] Error: {exc}")
