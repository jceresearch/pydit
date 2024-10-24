""" Testing check_duplicates using pytest """

import os
import sys
from datetime import datetime, date, timedelta
import pandas as pd


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import start_logging_info, business_calendar, first_and_end_of_month

logger = start_logging_info()


def test_fom_eom():
    """test the function for getting start and end of month"""
    assert first_and_end_of_month(date(2024, 2, 2), return_datetime=False)[1] == date(2024, 2, 29)
    assert first_and_end_of_month(date(2024, 8, 10))[0] == datetime(2024, 8, 1, 0, 0, 0)
    assert first_and_end_of_month(date(2024, 8, 10))[1] == datetime(2024, 8, 31, 23, 59, 59)
    assert first_and_end_of_month(date(2024, 8, 10), return_datetime=False)[0] == date(2024, 8, 1)
    assert first_and_end_of_month(date(2024, 8, 10), return_datetime=False)[1] == date(2024, 8, 31)

    # example testing one more second after the end of the month
    assert first_and_end_of_month(date(2024, 8, 10))[1] + timedelta(seconds=1) == datetime(
        2024, 9, 1, 0, 0, 0
    )


def test_basic_calculation():
    # A set of checks that the function is working properly
    cal = business_calendar(
        start_date=datetime(2010, 1, 1),
        end_date=datetime(2022, 1, 1),
        bus_start_time=8,
        bus_end_time=20,
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 9, 30, 6, 1, 0), pd.Timestamp(2019, 10, 1, 9, 0, 0)
        )
        == 13
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 10, 3, 10, 30, 0), pd.Timestamp(2019, 10, 3, 23, 30, 0)
        )
        == 10
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 8, 25, 10, 30, 0), pd.Timestamp(2019, 8, 27, 10, 0, 0)
        )
        == 2
    )

    # christmas and boxing day
    assert (
        cal.business_hours(
            pd.Timestamp(2019, 12, 25, 8, 0, 0), pd.Timestamp(2019, 12, 25, 17, 0, 0)
        )
        == 0
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 12, 26, 8, 0, 0), pd.Timestamp(2019, 12, 26, 17, 0, 0)
        )
        == 0
    )

    # another random business day
    assert (
        cal.business_hours(
            pd.Timestamp(2019, 12, 27, 8, 0, 0), pd.Timestamp(2019, 12, 27, 17, 0, 0)
        )
        == 9
    )

    # may bank holiday 2019
    assert (
        cal.business_hours(
            pd.Timestamp(2019, 6, 24, 5, 10, 44), pd.Timestamp(2019, 6, 24, 7, 39, 17)
        )
        == 0
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 6, 24, 5, 10, 44), pd.Timestamp(2019, 6, 24, 8, 29, 17)
        )
        == 0
    )
    assert (
        cal.business_hours(
            pd.Timestamp(2019, 6, 24, 5, 10, 44), pd.Timestamp(2019, 6, 24, 10, 0, 0)
        )
        == 2
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 4, 30, 21, 19, 0), pd.Timestamp(2019, 5, 1, 16, 17, 56)
        )
        == 8
    )

    assert (
        cal.business_hours(
            pd.Timestamp(2019, 4, 30, 21, 19, 0), pd.Timestamp(2019, 5, 1, 20, 17, 56)
        )
        == 12
    )
