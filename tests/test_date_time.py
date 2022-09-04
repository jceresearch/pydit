""" Testing check_duplicates using pytest """
import os
import sys

import numpy as np
import pandas as pd
import pytest


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import business_hours, start_logging_info

logger = start_logging_info()


# A set of checks that the function is working properly

assert (
    business_hours(
        pd.Timestamp(2019, 9, 30, 6, 1, 0),
        pd.Timestamp(2019, 10, 1, 9, 0, 0),
        day_series,
    )
    == 13
)
assert (
    business_hours(
        pd.Timestamp(2019, 10, 3, 10, 30, 0),
        pd.Timestamp(2019, 10, 3, 23, 30, 0),
        day_series,
    )
    == 10
)
assert (
    business_hours(
        pd.Timestamp(2019, 8, 25, 10, 30, 0),
        pd.Timestamp(2019, 8, 27, 10, 0, 0),
        day_series,
    )
    == 2
)
# christmas and boxing day
assert (
    business_hours(
        pd.Timestamp(2019, 12, 25, 8, 0, 0),
        pd.Timestamp(2019, 12, 25, 17, 0, 0),
        day_series,
    )
    == 0
)
assert (
    business_hours(
        pd.Timestamp(2019, 12, 26, 8, 0, 0),
        pd.Timestamp(2019, 12, 26, 17, 0, 0),
        day_series,
    )
    == 0
)
# another random business day
assert (
    business_hours(
        pd.Timestamp(2019, 12, 27, 8, 0, 0),
        pd.Timestamp(2019, 12, 27, 17, 0, 0),
        day_series,
    )
    == 9
)

# may bank holiday 2019
assert (
    business_hours(
        pd.Timestamp(2019, 6, 24, 5, 10, 44),
        pd.Timestamp(2019, 6, 24, 7, 39, 17),
        day_series,
    )
    == 0
)
assert (
    business_hours(
        pd.Timestamp(2019, 6, 24, 5, 10, 44),
        pd.Timestamp(2019, 6, 24, 8, 29, 17),
        day_series,
    )
    == 0
)
assert (
    business_hours(
        pd.Timestamp(2019, 6, 24, 5, 10, 44),
        pd.Timestamp(2019, 6, 24, 10, 0, 0),
        day_series,
    )
    == 2
)

assert (
    business_hours(
        pd.Timestamp(2019, 4, 30, 21, 19, 0),
        pd.Timestamp(2019, 5, 1, 16, 17, 56),
        day_series,
    )
    == 8
)
assert (
    business_hours(
        pd.Timestamp(2019, 4, 30, 21, 19, 0),
        pd.Timestamp(2019, 5, 1, 20, 17, 56),
        day_series,
    )
    == 12
)
