""" Test add_counts"""

import os
import sys

import pytest
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import count_related_key
from pydit import setup_logging

logger = setup_logging()


def test_count_related_key():
    """test for add counts in master and dimension table to check how they relate"""
    d1 = {"mkey": [1, 2, 3, 4], "mvalue": ["a", "b", "c", "d"]}

    # mkey and mkey2 are the same just different names to test how the
    # various ways of calling the function work
    d2 = {
        "tkey": [100, 101, 102, 103, 104, 105, 106],
        "mkey": [1, 1, 1, 2, 3, 3, 5],
        "mkey2": [1, 1, 1, 2, 3, 3, 5],
        "tvalue": [10.12, 20.4, 33.3, 45, 59.99, 60, -1],
    }

    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)

    # testing basic results
    df1, df2 = count_related_key(df1, df2, on="mkey")
    assert df1["count_fk_mkey"].to_list() == [3, 1, 2, 0]
    assert df2["count_fk_mkey"].to_list() == [1, 1, 1, 1, 1, 1, 0]

    # testing wrong imput fails gracefully
    with pytest.raises(ValueError):
        count_related_key(df1, df2)
    with pytest.raises(ValueError):
        count_related_key(df1, df2, left_on="mkey")

    # testing left_on and right_on
    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)
    df1, df2 = count_related_key(df1, df2, left_on="mkey", right_on="mkey2")
    assert df1["count_fk_mkey2"].to_list() == [3, 1, 2, 0]
    assert df2["count_fk_mkey"].to_list() == [1, 1, 1, 1, 1, 1, 0]

    # testing self counts
    assert df1["count_mkey"].to_list() == [
        1,
        1,
        1,
        1,
    ]  # There shouldnt be duplicates in df1 for the key
    assert df2["count_mkey2"].to_list() == [
        3,
        3,
        3,
        1,
        2,
        2,
        1,
    ]  # df2 has several duplicates for the key2, this is equivalent of countif on the main key


if __name__ == "__main__":
    # execute only if run as a script
    pass
