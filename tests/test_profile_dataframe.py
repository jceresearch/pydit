"""pytest test suite for profiling tools module"""

import os
import sys

import pandas as pd
from pandas import Timestamp
import numpy as np
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import (
    profile_dataframe,
    setup_logging,
)


logger = setup_logging()


@pytest.fixture
def df1():
    """Base DataFrame fixture 1"""
    data = {
        "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "col2": [1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
        "col3": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        "col4": ["a", np.nan, np.nan, "", "", "", 0, "0.00", "0.0", 9],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def df2():
    """Base DataFrame fixture 2"""
    df = pd.DataFrame(
        [
            [1, "INV-220001", Timestamp("2022-01-01 00:00:00"), "OPEN", 35.94, ""],
            [
                2,
                "INV-220002",
                Timestamp("2022-01-02 00:00:00"),
                "OPEN",
                99.99,
                "-5",
            ],
            [
                3,
                "INV-220003",
                Timestamp("2022-01-03 00:00:00"),
                "CANCELLED",
                13.0,
                "reinburse 10.5",
            ],
            [
                4,
                "INV-220003",
                Timestamp("2022-01-04 00:00:00"),
                "OPEN",
                float("nan"),
                "",
            ],
            [5, "INV-220005", Timestamp("2022-01-04 00:00:00"), "OPEN", 204.2, ""],
            [
                6,
                "INV-220006",
                Timestamp("2022-01-15 00:00:00"),
                "OPEN",
                -4.2,
                "discount",
            ],
            [
                7,
                float("nan"),
                Timestamp("2022-01-06 00:00:00"),
                float("nan"),
                0.0,
                "",
            ],
            [
                8,
                "INV-220007",
                Timestamp("2022-01-15 00:00:00"),
                "PENDING",
                50.4,
                "",
            ],
            [9, "", pd.NaT, "ERROR", 0.0, ""],
            [
                10,
                "INV-220007",
                Timestamp("2022-01-15 00:00:00"),
                "PENDING",
                50.4,
                "",
            ],
        ],
        columns=["id", "ref", "date_trans", "status", "amount", "notes"],
    )
    return df


def test_profile_dataframe(df1):
    """test the function for checking/profiling a dataframe"""
    res = profile_dataframe(df1, return_dict=True)
    assert res["col1"]["records"] == 10
    assert res["col1"]["count_unique"] == 10
    assert np.isnan(res["col1"]["empty_strings"])
    assert res["col1"]["dtype"] == np.dtype("int64")
    assert res["col1"]["std"] == pytest.approx(3.02765035)
    assert res["col1"]["sum_abs"] == 55
    assert res["col2"]["sum_abs"] == 55
    assert res["col2"]["sum"] == -53
    assert res["col2"]["min"] == -10
    assert res["col4"]["nans"] == 2
    assert res["col4"]["zeroes"] == 3


if __name__ == "__main__":
    pass
