""" pytest version of tests - WIP"""
import os
import sys

import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import add_counts_between_related_df
from pydit import setup_logging

logger = setup_logging()


def test_add_counts():
    """ test for add counts in master and dimension table to check how they relate"""
    d1 = {"mkey": [1, 2, 3, 4], "mvalue": ["a", "b", "c", "d"]}
    d2 = {
        "tkey": [100, 101, 102, 103, 104, 105, 106],
        "mkey": [1, 1, 1, 2, 3, 3, 5],
        "tvalue": [10.12, 20.4, 33.3, 45, 59.99, 60, -1],
    }

    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)
    add_counts_between_related_df(df1, df2, on="mkey")
    assert df1["count_mkey"].to_list() == [3, 1, 2, 0]
    assert df2["count_mkey"].to_list() == [1, 1, 1, 1, 1, 1, 0]
    assert add_counts_between_related_df(df1, df2) is None
    assert add_counts_between_related_df(df1, df2, left_on="mkey") is None
