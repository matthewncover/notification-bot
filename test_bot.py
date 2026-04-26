import os
from datetime import date

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test")
os.environ.setdefault("TELEGRAM_CHAT_ID", "test")

from bot import is_sweep_monday


def test_first_mondays():
    assert is_sweep_monday(date(2026, 5, 4))
    assert is_sweep_monday(date(2026, 6, 1))


def test_third_mondays():
    assert is_sweep_monday(date(2026, 5, 18))
    assert is_sweep_monday(date(2026, 6, 15))


def test_second_monday_is_not_sweep_day():
    assert not is_sweep_monday(date(2026, 5, 11))


def test_fourth_monday_is_not_sweep_day():
    assert not is_sweep_monday(date(2026, 5, 25))


def test_non_monday_is_not_sweep_day():
    assert not is_sweep_monday(date(2026, 5, 5))
