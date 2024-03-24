""" test of calendar functions"""

import os
import sys

import numpy as np


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import create_calendar, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = setup_logging()


def test_calendar():
    """test the calendar creation function"""
    res = create_calendar(start="2022-01-01", end="2022-01-31")
    print(res)
    assert res.shape[0] == 31
    assert res[res["date"] == "2022-01-24"]["weekday"].squeeze() == 0  # monday
    assert res[res["date"] == "2022-01-24"]["weekend"].squeeze() == False
    assert res[res["date"] == "2022-01-23"]["weekend"].squeeze() == True
    assert res[res["date"] == "2022-01-01"]["day_of_year"].squeeze() == 1
    assert (
        res[res["date"] == "2022-01-01"]["yyyyww"].squeeze() == 202152
    )  # ATTENTION THIS WILL WORK FOR SORTING WEEKS ON AXIS BUT NOT WEEK


if __name__ == "__main__":
    # test_calendar()
    pass
