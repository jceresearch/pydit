""" Test module for groupby_text.py """
import os
import sys

import numpy as np
import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import groupby_text


@pytest.fixture
def df():
    """Base DataFrame fixture"""
    data = {
        "team": ["teamA", "teamA", "teamA", "teamA", "teamA", "teamB", "teamC"],
        "purid": ["P01", "P01", "P01", "P02", "P02", "P03", "P03"],
        "apprid": [1, 2, 3, 4, 5, 6, 7],
        "appr": ["ok", "ok", "rejected", "ok", " ", "Error", "ok",],
        "user": ["user1", "user2", "user1", "user2", "", np.nan, "user3"],
    }
    return pd.DataFrame(data)


def test_groupby_bad_formed(df):
    """test for badly formed calls"""


def test_groupby_text(df):
    """Test ouptut with exmples that should work, various aggregation options"""

    res = groupby_text(df, "purid", value_cols=["appr", "user"])
    exp = ["ok user1\nok user2\nrejected user1", "ok user2", "Error \nok user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team", "purid"], value_cols=["apprid", "appr", "user"])
    exp = [
        "1 ok user1\n2 ok user2\n3 rejected user1",
        "4 ok user2\n5",
        "6 Error",
        "7 ok user3",
    ]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team", "purid"], value_cols=["appr", "user"])
    exp = ["ok user1\nok user2\nrejected user1", "ok user2", "Error", "ok user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team"], value_cols=["user"], row_separator=" ")
    exp = ["user1 user2 user1 user2", "", "user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team"], value_cols=["purid", "appr"], row_separator=" ")
    exp = ["P01 ok P01 ok P01 rejected P02 ok P02", "P03 Error", "P03 ok"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["purid"], value_cols=["apprid", "appr"], row_separator="|")
    exp = ["1 ok|2 ok|3 rejected", "4 ok|5", "6 Error|7 ok"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, "purid", value_cols="appr", row_separator="|")
    exp = ["ok|ok|rejected", "ok|", "Error|ok"]
    assert list(res["groupby_text"]) == exp


if __name__ == "__main__":
    pass
