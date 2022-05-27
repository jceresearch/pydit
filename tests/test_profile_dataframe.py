""" pytest test suite for profiling tools module"""
import os
import sys

import pandas as pd
from pandas import Timestamp

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import (
    profile_dataframe,
    setup_logging,
)


logger = setup_logging()


def test_profile_dataframe():
    """test the function for checking/profiling a dataframe"""
    # test that passing one column will fail gracefully
    df = pd.DataFrame(
        [
            [1, "INV-220001", Timestamp("2022-01-01 00:00:00"), "OPEN", 35.94, ""],
            [2, "INV-220002", Timestamp("2022-01-02 00:00:00"), "OPEN", 99.99, "-5",],
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
            [7, float("nan"), Timestamp("2022-01-06 00:00:00"), float("nan"), 0.0, "",],
            [8, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, "",],
            [9, "", pd.NaT, "ERROR", 0.0, ""],
            [10, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, "",],
        ],
        columns=["id", "ref", "date_trans", "status", "amount", "notes"],
    )
    assert profile_dataframe(df["id"]) is None
    assert "This test is still not fully implemented" == False
