import logging
import os
import sys
import time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import requests
import schedule

TZ = ZoneInfo("America/Los_Angeles")
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SUNDAY_MSG = (
    "\U0001F9F9 Street sweeping tomorrow (Monday).\n"
    "• If your car is on the FAR side (across the street): move it TONIGHT — "
    "sweeping there runs 6 AM – 10 AM.\n"
    "• If your car is on the NEAR side (in front of the house): move it "
    "between 9:30 AM and 10 AM tomorrow — sweeping there runs 10 AM – 2 PM."
)
MORNING_MSG = (
    "\U0001F9F9 Street sweeping on the NEAR side (in front of the house) starts at 10 AM. "
    "If your car is parked there, move it now (between 9:30 and 10 AM)."
)


def is_sweep_monday(d: date) -> bool:
    return d.weekday() == 0 and (d.day - 1) // 7 in (0, 2)


def send(text: str) -> None:
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=15,
    )
    r.raise_for_status()


def today_local() -> date:
    return datetime.now(TZ).date()


def sunday_check() -> None:
    if is_sweep_monday(today_local() + timedelta(days=1)):
        logging.info("sending sunday reminder")
        send(SUNDAY_MSG)


def morning_check() -> None:
    if is_sweep_monday(today_local()):
        logging.info("sending morning reminder")
        send(MORNING_MSG)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    if "--test" in sys.argv:
        send("✅ Test ping from sweep bot.")
        return
    schedule.every().day.at("20:00", "America/Los_Angeles").do(sunday_check)
    schedule.every().day.at("09:30", "America/Los_Angeles").do(morning_check)
    logging.info("scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
