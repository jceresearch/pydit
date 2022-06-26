""" pytest version of tests - WIP"""
import os
import sys

import pandas as pd


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import merge_force_suffix, setup_logging

logger = setup_logging()


def test_merge_basic():
    """testing the basic functionality with correct inputs"""
    df1 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    df2 = pd.DataFrame({"a": [1, 2, 3], "c": [4, 5, 6], "d": [7, 8, 9]})

    res1 = merge_force_suffix(df1, df2, on="a", suffixes=("_1", "_2"))
    assert list(res1.columns) == ["a", "b_1", "c_1", "c_2", "d_2"]
    assert res1.shape == (3, 5)
    res2 = merge_force_suffix(
        df1, df2, left_on="b", right_on="c", suffixes=("_1", "_2")
    )
    assert list(res2.columns) == ["a_1", "b", "c_1", "a_2", "c", "d_2"]
    assert res2.shape == (3, 6)
    res3 = merge_force_suffix(
        df1, df2, left_on="a", right_on="a", suffixes=("_1", "_2")
    )
    assert list(res3.columns) == ["a", "b_1", "c_1", "c_2", "d_2"]
    assert res3.shape == (3, 5)


if __name__ == "__main__":
    test_merge_basic()
