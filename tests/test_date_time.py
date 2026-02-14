"""Testing check_duplicates using pytest"""

import os
import sys
from datetime import datetime, date, timedelta
import pandas as pd
import pytest


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import business_calendar, first_and_end_of_month, date_relative_in_words


def test_first_and_end_of_month_eom():
    """test the function for getting start and end of month"""
    assert first_and_end_of_month(date(2024, 2, 2), return_datetime=False)[1] == date(
        2024, 2, 29
    )
    assert first_and_end_of_month(date(2024, 8, 10))[0] == datetime(2024, 8, 1, 0, 0, 0)
    assert first_and_end_of_month(date(2024, 8, 10))[1] == datetime(
        2024, 8, 31, 23, 59, 59
    )
    assert first_and_end_of_month(date(2024, 8, 10), return_datetime=False)[0] == date(
        2024, 8, 1
    )
    assert first_and_end_of_month(date(2024, 8, 10), return_datetime=False)[1] == date(
        2024, 8, 31
    )

    # example testing one more second after the end of the month
    assert first_and_end_of_month(date(2024, 8, 10))[1] + timedelta(
        seconds=1
    ) == datetime(2024, 9, 1, 0, 0, 0)


@pytest.fixture(scope="module")
def cal():
    return business_calendar(
        start_date=datetime(2010, 1, 1),
        end_date=datetime(2040, 1, 1),
        bus_start_time=8,
        bus_end_time=20,
    )


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (
            pd.Timestamp(2019, 9, 30, 6, 1, 0),
            pd.Timestamp(2019, 10, 1, 9, 0, 0),
            13,
        ),
        (
            pd.Timestamp(2019, 10, 3, 10, 30, 0),
            pd.Timestamp(2019, 10, 3, 23, 30, 0),
            10,
        ),
        (
            pd.Timestamp(2019, 8, 25, 10, 30, 0),
            pd.Timestamp(2019, 8, 27, 10, 0, 0),
            2,
        ),
        (
            pd.Timestamp(2019, 12, 25, 8, 0, 0),
            pd.Timestamp(2019, 12, 25, 17, 0, 0),
            0,
        ),
        (
            pd.Timestamp(2019, 12, 26, 8, 0, 0),
            pd.Timestamp(2019, 12, 26, 17, 0, 0),
            0,
        ),
        (
            pd.Timestamp(2019, 12, 27, 8, 0, 0),
            pd.Timestamp(2019, 12, 27, 17, 0, 0),
            9,
        ),
        (
            pd.Timestamp(2019, 6, 24, 5, 10, 44),
            pd.Timestamp(2019, 6, 24, 7, 39, 17),
            0,
        ),
        (
            pd.Timestamp(2019, 6, 24, 5, 10, 44),
            pd.Timestamp(2019, 6, 24, 8, 29, 17),
            0,
        ),
        (
            pd.Timestamp(2019, 6, 24, 5, 10, 44),
            pd.Timestamp(2019, 6, 24, 10, 0, 0),
            2,
        ),
        (
            pd.Timestamp(2019, 4, 30, 21, 19, 0),
            pd.Timestamp(2019, 5, 1, 16, 17, 56),
            8,
        ),
        (
            pd.Timestamp(2019, 4, 30, 21, 19, 0),
            pd.Timestamp(2019, 5, 1, 20, 17, 56),
            12,
        ),
    ],
    ids=[
        "overnight_split",
        "same_day_clip_end",
        "weekend_to_weekday",
        "christmas_day",
        "boxing_day",
        "regular_business_day",
        "pre_open_to_pre_open",
        "pre_open_to_before_open",
        "pre_open_to_mid_morning",
        "after_hours_to_midday",
        "after_hours_to_day_end",
    ],
)
def test_basic_calculation(cal, start, end, expected):
    # A set of checks that the function is working properly
    assert cal.business_hours(start, end) == expected


@pytest.mark.parametrize(
    "input_date,reference_datetime,expected",
    [
        (None, datetime(2026, 2, 14, 12, 0, 0), ""),
        ("", datetime(2026, 2, 14, 12, 0, 0), ""),
        ([], datetime(2026, 2, 14, 12, 0, 0), ""),
        ("\n", datetime(2026, 2, 14, 12, 0, 0), ""),
        ("not-a-date", datetime(2026, 2, 14, 12, 0, 0), ""),
        ("2026-02-10", datetime(2026, 2, 14, 12, 0, 0), "within a week ago"),
        ("2026-02-18", datetime(2026, 2, 14, 12, 0, 0), "within a week from now"),
        ("2026-01-20", datetime(2026, 2, 14, 12, 0, 0), "25 days ago"),
        ("2026-03-04", datetime(2026, 2, 14, 12, 0, 0), "in 18 days"),
        ("2025-12-31", datetime(2026, 2, 14, 12, 0, 0), "2 months ago"),
        ("2026-05-01", datetime(2026, 2, 14, 12, 0, 0), "in 3 months"),
        ("2023-12-01", datetime(2026, 2, 14, 12, 0, 0), "more than two years ago"),
        ("2028-03-01", datetime(2026, 2, 14, 12, 0, 0), "in more than two years"),
    ],
)
def test_date_relative_in_words(input_date, reference_datetime, expected):
    """Test date_relative_in_words for blank, day, month and >2 years ranges."""
    assert date_relative_in_words(input_date, reference_datetime) == expected
