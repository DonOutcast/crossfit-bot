import pytest
import datetime

from model import AioCalendar


def test_init():
    date_calendar = AioCalendar()
    assert date_calendar.year == datetime.datetime.now().year
    assert date_calendar.month == datetime.datetime.now().month
    assert 1 == 1
