""" test of calendar functions"""

import os
import sys
from datetime import date, datetime, timedelta


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import create_calendar, setup_logging, fom_eom


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



def test_fom_eom():
    """test the function for getting start and end of month"""
    assert fom_eom(date(2024, 2, 2), return_datetime=False)[1] == date(2024, 2, 29)
    assert fom_eom(date(2024, 8, 10))[0] == datetime(2024, 8, 1, 0, 0, 0)
    assert fom_eom(date(2024, 8, 10))[1] == datetime(2024, 8, 31, 23, 59, 59)
    assert fom_eom(date(2024, 8, 10), return_datetime=False)[0] == date(2024, 8, 1)
    assert fom_eom(date(2024, 8, 10), return_datetime=False)[1] == date(2024, 8, 31)

    #example testing one more second after the end of the month
    assert fom_eom(date(2024, 8, 10))[1] + timedelta(seconds=1) == datetime(2024, 9, 1, 0, 0, 0)










if __name__ == "__main__":
    # test_calendar()
    pass
