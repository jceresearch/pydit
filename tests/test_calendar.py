"""test of calendar functions"""

import os
import sys
from datetime import date, datetime
import numpy as np
import pandas as pd


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit.wrangling import create_calendar, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = setup_logging()


def test_calendar_ranges():
    """test the calendar creation function"""
    res = create_calendar(start=date(2024, 1, 1), end=date(2024, 12, 31))
    assert res.shape[0] == 366
    # now with datetime
    res = create_calendar(start=datetime(2024, 1, 1), end=datetime(2024, 12, 31))
    assert res.shape[0] == 366
    # now with some extra hours and minutes
    res = create_calendar(
        start=datetime(2024, 1, 1, 12, 30), end=datetime(2024, 12, 31, 12, 30)
    )
    assert res.shape[0] == 366
    assert res["date_dt"].iloc[0] == pd.Timestamp(2024, 1, 1)
    assert res["date_dt"].iloc[0] == datetime(2024, 1, 1)
    assert res["date_dt"].iloc[-1] == datetime(2024, 12, 31)


def test_calendar_values():
    """test the calendar creation function"""
    res = create_calendar(start="2022-01-01", end="2022-01-31")
    assert res.shape[0] == 31
    assert res[res["date"] == "2022-01-24"]["weekday"].squeeze() == 1  # monday
    assert res[res["date"] == "2022-01-24"]["weekend"].squeeze() == False
    assert res[res["date"] == "2022-01-23"]["weekend"].squeeze() == True
    assert res[res["date"] == "2022-01-01"]["day_of_year"].squeeze() == 1
    assert (
        res[res["date"] == "2022-01-01"]["yyyyww"].squeeze() == 202152
    )  # ATTENTION THIS WILL WORK FOR SORTING WEEKS ON AXIS BUT NOT WEEK


if __name__ == "__main__":
    # test_calendar()
    pass
