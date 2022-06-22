"""Test for truncate datetime to a specific unit"""

from datetime import datetime
import os
import sys

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import truncate_datetime_dataframe, setup_logging

logger = setup_logging()


def test_truncate_datetime_dataframe_invalid_datepart():
    """Checks if a ValueError is appropriately raised when datepart is
    not a valid enumeration.
    """
    x = datetime(2022, 3, 21, 9, 1, 15, 666)
    df = pd.DataFrame({"dt": [x], "foo": [np.nan]}, copy=False)
    with pytest.raises(ValueError, match=r"invalid `datepart`"):
        truncate_datetime_dataframe(df, "INVALID")


def test_truncate_datetime_dataframe_all_parts():
    """Test for truncate_datetime_dataframe, for all valid dateparts.
    Also only passes if `truncate_datetime_dataframe` method is idempotent.
    """
    x = datetime(2022, 3, 21, 9, 1, 15, 666)
    df = pd.DataFrame({"dt": [x], "foo": [np.nan]}, copy=False)

    result = truncate_datetime_dataframe(df, "second")
    assert result.loc[0, "dt"] == datetime(2022, 3, 21, 9, 1, 15, 0)
    result = truncate_datetime_dataframe(df, "minute")
    assert result.loc[0, "dt"] == datetime(2022, 3, 21, 9, 1)
    result = truncate_datetime_dataframe(df, "HOUR")
    assert result.loc[0, "dt"] == datetime(2022, 3, 21, 9)
    result = truncate_datetime_dataframe(df, "Day")
    assert result.loc[0, "dt"] == datetime(2022, 3, 21)
    result = truncate_datetime_dataframe(df, "month")
    assert result.loc[0, "dt"] == datetime(2022, 3, 1)
    result = truncate_datetime_dataframe(df, "yeaR")
    assert result.loc[0, "dt"] == datetime(2022, 1, 1)


# bad data


def test_truncate_datetime_dataframe_do_nothing():
    """Ensure nothing changes (and no errors raised) if there are no datetime-
    compatible columns.
    """
    data = {
        "a": [1, 0],
        "b": ["foo", ""],
        "c": [np.nan, 3.0],
        "d": [True, False],
    }

    df = pd.DataFrame(data)
    result = truncate_datetime_dataframe(df, "year")
    expected = pd.DataFrame(data)
    assert_frame_equal(result, expected)


def test_truncate_datetime_containing_NaT():
    """Ensure NaT is ignored safely (no-op) and no TypeError is thrown."""
    x = datetime(2022, 3, 21, 9, 1, 15, 666)
    df = pd.DataFrame({"dt": [x, pd.NaT], "foo": [np.nan, 3]})
    expected = pd.DataFrame(
        {"dt": [x.replace(microsecond=0), pd.NaT], "foo": [np.nan, 3]}
    )

    result = truncate_datetime_dataframe(df, "second")
    assert_frame_equal(result, expected)
